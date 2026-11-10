# Engineering lessons

Lessons recovered from the notes of a discarded third-party automation
tool, kept here instead of deleted. Each entry carries the commit that landed
the change in this repository, so a proposal can be located in the history
before the same change is proposed again. Dates are landing dates taken from
`git log`; the order below is the order the notes recorded, not a re-sorting.

## Performance

### 2025-05-15 - Concurrent Session Revocation
**Learning:** Sequential async calls for disconnecting multiple backends (e.g., Telethon clients) can cause significant delays because each disconnect involves an MTProto roundtrip. Using `asyncio.gather` reduces this latency to a single roundtrip.
**Action:** Always use `asyncio.gather` when performing bulk operations that involve network I/O or other awaitable tasks, especially for cleanup or shutdown procedures.
### 2025-06-30 - Parallel KV Session Store Loading
**Learning:** `load_all` on a credential backend with individual `load()` operations suffers from an N+1 query bottleneck. Since the underlying PBKDF2 key derivations using the `cryptography` library release the GIL, thread pools provide significant speedups even in Python, overlapping both I/O and heavy crypto compute.
**Action:** Parallelize bulk load operations over single-item APIs using `ThreadPoolExecutor.map()` to avoid sequential blocking. Combine results with `zip(..., strict=True)`.
### 2025-07-28 - Parallel KV Pending OTP Store Loading and Write Skipping
**Learning:** `cleanup_expired` on a credential backend using individual `load()` operations suffers from an N+1 query bottleneck because of heavy PBKDF2 cryptography computations. It's also wasteful to perform `save()` when no keys have expired. Parallelization using a thread pool resolves the read bottleneck, and adding an early return skips unnecessary network/IO bounds. However, when doing this, make sure to use `list()` for `_load_index()` to prevent runtime iterator modification crashes during a zip iteration.
**Action:** When working on periodic cleanup functions with heavy read burdens, use `ThreadPoolExecutor` to speed up the loop, and use an early return to stop wasteful DB writes. Always copy indices (e.g. `list(subs)`) if they might be pruned in the parallelization's consumption loop.
### 2025-08-15 - Caching dynamically imported functions in hot paths
**Learning:** Python's `import` statement inside a function incurs a small overhead (checking `sys.modules`) on every call. In highly-called "hot path" functions like `get_backend()` that dispatch every MCP tool invocation, this repeated import evaluation adds unnecessary execution time.
**Action:** When a deferred import is required (e.g. to avoid circular dependencies or for conditional multi-user modes), lazy-load it once into a global or closure variable (e.g. `_get_current_backend`). Subsequent calls should use the cached reference, which provides a ~2.4x speedup for the function execution compared to repeating the dynamic import.
### 2025-08-30 - Internalizing Thread Offloading for Blocking I/O
**Learning:** In asynchronous backends, internal helper methods that perform blocking filesystem I/O (like `os.open`, `os.chmod`, or file-backed key-value lookups) can block the main asyncio event loop if not properly offloaded. While the offloading could be done at the call site, doing so clutters the call site and relies on callers to remember the implementation detail.
**Action:** Always refactor internal helper methods that perform blocking I/O to be `async def`. Wrap their synchronous logic in a nested function and internally offload it using `await asyncio.to_thread()`. This improves API clarity and ensures non-blocking behavior wherever the method is invoked.
### 2025-08-31 - O(1) Existence Checks for Encrypted Stores
**Learning:** Checking for session existence using bulk data retrieval methods like `load_all()` incurs massive overhead from N+1 decryption operations (e.g., PBKDF2) in the Cryptographic KV Store, even when no sessions exist, due to ThreadPoolExecutor initialization and index iteration.
**Action:** When checking if any records exist or before processing bulk operations like `restore_sessions` or `cleanup_expired`, always implement and utilize index-only checks like `has_any()` to achieve O(1) existence verification and skip expensive bulk loads when empty.

## Security

### 2025-02-27 - Fix DoS via memory exhaustion in fetch_url_safely
**Vulnerability:** fetch_url_safely used httpx.AsyncClient.get which loads the entire response into memory at once, creating a risk for Denial of Service (DoS) via Out-Of-Memory (OOM) attacks if a malicious or large file is fetched.
**Learning:** External URLs should be fetched with size limits and streaming to prevent memory exhaustion, as even validated internal IPs/URLs can return massive payloads.
**Prevention:** Always use httpx.stream and iterate over chunks (`aiter_bytes`) while enforcing a strict `max_size` limit on the accumulated data and checking the Content-Length header.
### 2025-02-24 - Cryptographically secure token generation
**Vulnerability:** Use of `os.urandom(32).hex()` for secret token generation.
**Learning:** While `os.urandom` is cryptographically secure, using the explicit `secrets` module (e.g. `secrets.token_hex(32)`) conveys a clearer security intent, is less prone to misuse, and aligns with modern Python security best practices.
**Prevention:** Use `secrets.token_hex()` or `secrets.token_urlsafe()` instead of raw `os.urandom` where appropriate.

### 2024-05-18 - SSRF via IPv6 Unspecified Address (::)
**Vulnerability:** The URL validation logic correctly blocked the IPv4 unspecified address `0.0.0.0` but failed to block its IPv6 equivalent `::`. This allowed SSRF requests to bypass the filter and target `localhost` on systems with IPv6 enabled.
**Learning:** Hardcoded string checks (like `hostname in {"0.0.0.0"}`) and IPv4-only IP network blocks are insufficient when IPv6 is available, as attackers can use IPv6 variants (like `::`) to achieve the same routing behavior.
**Prevention:** Always include the IPv6 equivalent `::/128` (unspecified) in blocked internal networks alongside `0.0.0.0/8`, and ensure string-based early filters catch `::`.
### 2025-02-28 - Fix DoS via memory exhaustion in bot_backend download_media
**Vulnerability:** `BotBackend.download_media` used `httpx.AsyncClient.get` which loads the entire response into memory at once. If a bot is tricked into downloading a massive file, this could lead to Out-Of-Memory (OOM) Denial of Service (DoS).
**Learning:** Even internal API wrappers (like Telegram Bot API wrappers) must treat large file downloads securely, especially if the input `file_id` is passed by users (e.g. from an MCP query).
**Prevention:** Always stream media downloads using `httpx.stream`, check `Content-Length`, enforce a `max_size` limit, and iterate over the response chunks using `aiter_bytes()`. Avoid using `asyncio.to_thread` for every small chunk, relying instead on OS-level buffering to minimize overhead.
### 2025-10-24 - Fix DoS via memory exhaustion in bot_backend send_media
**Vulnerability:** `BotBackend.send_media` loaded entire local files into memory at once using `path.read_bytes()`. An attacker could exploit this by instructing the MCP bot to send an excessively large file, leading to an Out-Of-Memory (OOM) Denial of Service (DoS) attack that crashes the server.
**Learning:** File read operations must enforce a strict size limit before loading contents into memory, even for local files validated for path traversal, as local files can be gigabytes in size.
**Prevention:** Always check `path.stat().st_size` against a `max_size` limit (e.g., 50MB for Telegram Bot API) before reading the entire file into memory using `read_bytes()`.

### 2025-02-28 - Fix DoS via memory exhaustion in bot_backend send_media
**Vulnerability:** `BotBackend.send_media` loaded entire local files into memory at once using `path.read_bytes()`. An attacker could exploit this by instructing the MCP bot to send an excessively large file, leading to an Out-Of-Memory (OOM) Denial of Service (DoS) attack that crashes the server.
**Learning:** Even with an upfront size limit check (e.g. `path.stat().st_size`), loading files into memory instead of streaming them is dangerous, especially in multi-user environments where concurrent requests could quickly exhaust container memory limits.
**Prevention:** Always stream media uploads by passing an open file handle (`open(path, 'rb')`) instead of the file content string/bytes directly, especially to HTTP clients like `httpx` which natively support chunked streaming from file objects. Use a `finally` block to ensure the file handle is closed correctly.

## Accessibility and UX

### 2024-06-25 - Improve ARIA associations in credential forms
**Learning:** For dynamic/conditionally-visible elements like status boxes or inline errors (e.g. `status-box`, `step-error`), it is completely safe and highly recommended to associate them proactively via `aria-describedby` directly on the `<input>` fields, even if the error blocks are initially empty or styled as `display: none`. Furthermore, strictly decorative strings like "Required" visual badges adjacent to natively `<input required>` fields should have `aria-hidden="true"` applied to avoid screen readers announcing "Required required" redundantly.
**Action:** Always verify if a native `required` attribute exists on inputs before adding visual "Required" text. If it does, ensure the visual text is masked with `aria-hidden="true"`. Pre-wire inputs to their respective alert/status `div` elements with `aria-describedby` during HTML templating.
### 2024-05-05 - Focus First Invalid Input on Form Validation Failure
**Learning:** Bringing focus to the first invalid input when client-side form validation fails is a low-effort, high-impact a11y/UX pattern that works natively without relying solely on screen reader ARIA live regions to announce errors.
**Action:** Always add `.focus()` calls when interrupting form submissions with JS validation logic.

### 2024-06-25 - Focus Management in Async Forms
**Learning:** In asynchronous form flows (e.g., fetch API calls in `credential_form.py`), failing to explicitly restore keyboard focus to the input field within error handling branches (like `.catch()` blocks) causes screen readers and keyboard users to lose their context upon network or validation failures. This creates a frustrating experience where users have to navigate back to the input to correct the issue.
**Action:** Always ensure that keyboard focus is returned to the relevant interactive element (e.g., `inputEl.focus();`) after an asynchronous operation fails and the UI is reset.

### 2024-07-28 - W3C ARIA Tablist Pattern Keyboard Navigation
**Learning:** For custom tabbed interfaces (like the Bot Mode / User Mode toggle), setting `role="tablist"` and `role="tab"` is not enough for complete accessibility. Users relying on keyboard navigation expect the W3C ARIA Tablist pattern, which specifically dictates that `Tab` moves focus *into* the active tab, and `ArrowLeft` / `ArrowRight` navigate *between* tabs. Without this keyboard event handling, custom tab arrays remain difficult or confusing to navigate for screen reader and keyboard-only users.
**Action:** When implementing custom tabs, always include a W3C-compliant roving `tabindex` (setting `tabindex="0"` on the active tab and `tabindex="-1"` on inactive tabs) and add `keydown` event listeners to handle `ArrowLeft` and `ArrowRight` keys for seamlessly shifting focus and selection between the tab buttons.

### 2024-07-28 - Contrast Requirements for Dark Themes
**Learning:** Text using color `#666` fails WCAG AA 4.5:1 contrast requirements when placed against dark-themed backgrounds such as `#1a1a1a`.
**Action:** When designing dark themes, ensure that subtle or secondary text elements (like `.server-id` and `.help-text`) are upgraded to at least `#888` or `#999` to maintain readability and accessibility standards.

### 2024-07-29 - Clear Validation State on Input
**Learning:** Lingering error states (`aria-invalid="true"` or visible error messages) are frustrating when users begin to correct the issue but the UI continues shouting at them until the next submit.
**Action:** Always attach `input` event listeners to form fields to actively strip validation styling and hide inline error messages as soon as the user resumes typing.
### 2024-05-19 - Password Visibility Toggles for API Keys
**Learning:** Password visibility toggles (Show/Hide buttons) are not just helpful for user passwords, but provide a critical UX improvement for long API keys (like Bot Tokens). Users often paste partial keys or experience issues verifying successful copy-pastes, leading to frustrating auth failures.
**Action:** Always consider adding "Show/Hide" toggle buttons to `type="password"` fields that accept long API keys or tokens to allow users to visually verify their input before submitting.

### 2024-07-30 - ARIA Pressed for State Toggles
**Learning:** State toggle buttons (like password visibility Show/Hide toggles) need to utilize the `aria-pressed` attribute to properly communicate their active state to screen readers.
**Action:** Ensure toggle buttons include `aria-pressed="false"` initially and dynamically update to `true` when activated.

### 2024-07-30 - Color Scheme Meta Tag for Dark Themes
**Learning:** Dark-themed HTML templates must explicitly include `<meta name="color-scheme" content="dark">` to ensure native browser elements (like scrollbars and autofill dropdowns) adapt to the dark aesthetic instead of defaulting to a jarring light mode.
**Action:** Always include the `<meta name="color-scheme" content="dark">` tag in the `<head>` of dark-themed HTML documents.

### 2024-07-29 - Enhancing State Change UX with Subtle Animations
**Learning:** Instantaneous layout shifts or state changes (e.g., switching between tabs or dynamically surfacing complex multi-step forms) can feel jarring or unpolished, potentially increasing cognitive load as users mentally trace the new UI structure. Subtle animations, such as a quick fade-in with a slight downward translation (`translateY`), soften these transitions, providing a much smoother, higher-quality interaction.
**Action:** Apply lightweight, short-duration CSS `@keyframes` animations (e.g., `<0.3s`) to significant DOM additions or view transitions, particularly when toggling `.active` panel states or appending new user prompts.

### 2026-06-21 - Prevent Hover Styles on Disabled Interactive Elements
**Learning:** Applying `:hover` styles universally to interactive elements like buttons and tabs creates confusing visual feedback when those elements are `disabled`. Users may interpret the hover effect as an indication that the element is clickable, leading to frustration.
**Action:** When styling `:hover` states, always use the `:not(:disabled):hover` pseudo-class (or equivalent) to ensure interactive styling is only applied to active elements. Additionally, explicitly style `:disabled` states (e.g. `opacity: 0.5; cursor: not-allowed;`) to make the disabled status visually unambiguous.

### 2026-06-21 - Prefer Native Labels over ARIA for Dynamic Prompts
**Learning:** Using a generic `<p>` tag combined with `aria-labelledby` on an input for dynamic forms (like multi-step OTP prompts) provides accessible names to screen readers but misses a key physical usability benefit. A semantic `<label>` properly associated with an input using the `for`/`id` relationship increases the clickable/tap area, allowing users to click the text prompt itself to focus the input field.
**Action:** When dynamically generating form elements in JavaScript, always prefer creating a `<label>` element and setting its `for` attribute to the input's `id` instead of relying on `aria-labelledby` with generic block elements.
### 2024-08-01 - Active States for Interactive Elements
**Learning:** Adding subtle `:active` pseudo-class styles with `transform: scale()` provides tactile visual feedback for interactive elements (like buttons and tabs), making the interface feel more responsive.
**Action:** When creating custom buttons or interactive tabs, define an `:active` state using `:not(:disabled):active` and apply a slight scale down (e.g., `transform: scale(0.98)`) and ensure `transform` is included in the element's `transition` property.
### 2024-08-05 - Reduced Motion Accessibility
**Learning:** Animations and transitions can be uncomfortable or inaccessible for users with vestibular disorders or motion sensitivities. Relying solely on CSS transitions and keyframes without respecting the operating system's reduced motion settings is a widespread accessibility failure.
**Action:** Always include a `@media (prefers-reduced-motion: reduce)` block in custom CSS to globally neutralize animations (e.g., setting `animation-duration: 0.01ms !important; transition-duration: 0.01ms !important;`) for environments where users have requested reduced motion.

### 2024-11-20 - Dual-Channel Validation Feedback
**Learning:** Relying solely on color (like `#f87171` red borders) for `aria-invalid` states is insufficient for users with color vision deficiencies and can be easily missed. Providing dual-channel feedback by combining color with a subtle, non-disruptive motion animation (like a short horizontal `@keyframes shake`) significantly improves error discoverability and accessibility.
**Action:** When implementing client-side validation, always apply a subtle motion animation (e.g., `shake 0.4s ease-in-out`) alongside color changes to `.field-input[aria-invalid="true"]` elements to provide robust, dual-channel error feedback, while ensuring it respects `prefers-reduced-motion: reduce`.
### 2024-05-19 - Use field-group and semantic labels for dynamic prompts
**Learning:** For dynamic form inputs (like OTP steps), ensure visual consistency and accessibility by wrapping the input and label in a `.field-group` container, applying the `.field-label` class to the semantic `<label>`, and explicitly appending `<span class="required-badge" aria-hidden="true">Required</span>` to mandatory fields instead of rendering prompts as title headers.
**Action:** Always maintain uniform visual hierarchy by matching the dynamic step form markup structure with the main form's styling pattern.

### 2024-11-21 - Disable Associated Utility Controls During Form Submission
**Learning:** Leaving auxiliary interactive elements (like password visibility toggles) enabled while the primary inputs and submit button are disabled in a loading state creates an inconsistent UI state and can lead to confusing behavior during async operations.
**Action:** Always ensure that all interactive utility elements associated with a form are explicitly disabled alongside the main inputs and submit button when transitioning into a disabled/loading state, and properly re-enabled when the state resets.

### 2024-11-21 - Dual-Channel Validation for Server Errors
**Learning:** While client-side validation correctly applied dual-channel feedback (color + shake animation) via `aria-invalid="true"`, server-side and network errors simply focused the input and showed a text error. This inconsistency meant users who bypassed client validation or hit server errors didn't receive the same robust accessibility feedback.
**Action:** When handling server-side validation or network errors that relate to an input field, always apply `aria-invalid="true"` to that field before focusing it, ensuring consistent dual-channel feedback regardless of where the validation failed.

### 2024-11-21 - Synchronize ARIA Labels When Reusing DOM Containers
**Learning:** Reusing DOM containers for dynamic form steps (e.g., OTP or password prompts) can lead to desynchronized accessibility states if all associated attributes are not reset. While visual properties like `textContent` might be reset when re-initializing the view, missing updates to attributes like `aria-label` can leave screen readers announcing stale and confusing states (e.g., a button displaying "Show" but announcing "Hide password").
**Action:** When dynamically resetting or reusing stateful UI components, ensure that invisible attributes like `aria-label` are explicitly reset alongside their visible counterparts (like `textContent` and `aria-pressed`) to prevent out-of-sync UI states.

### 2025-02-09 - Disabled State Tooltips for Utility Controls
**Learning:** When utility controls (like a password visibility toggle) are dynamically disabled alongside a main form submission, users relying on screen readers or mouse hover can be confused as to why the control is suddenly unresponsive. Adding a dynamic `title` attribute (e.g., "Disabled during submission") provides immediate, helpful context for the disabled state, improving discoverability.
**Action:** Always provide explanatory `title` tooltips for auxiliary buttons when their disabled state is tied to a broader async operation (like form submission), and dynamically swap the tooltip text back to the action description when re-enabled.

### 2024-07-29 - Enhancing State Change UX with Subtle Animations
**Learning:** Instantaneous layout shifts or state changes (e.g., switching between tabs or dynamically surfacing complex multi-step forms) can feel jarring or unpolished, potentially increasing cognitive load as users mentally trace the new UI structure. Subtle animations, such as a quick fade-in with a slight downward translation (`translateY`), soften these transitions, providing a much smoother, higher-quality interaction.
**Action:** Apply lightweight, short-duration CSS `@keyframes` animations (e.g., `<0.3s`) to significant DOM additions or view transitions, particularly when toggling `.active` panel states or appending new user prompts.
