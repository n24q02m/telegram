# CHANGELOG

<!-- version list -->

## v4.23.0 (2026-10-27)


## v4.23.0-beta.1 (2026-10-27)

### Bug Fixes

- Align registry and plugin metadata with renamed identity
  ([#1114](https://github.com/n24q02m/telegram/pull/1114),
  [`5b96bcc`](https://github.com/n24q02m/telegram/commit/5b96bcc23d8c251e398144ebbf3839fb73a0bf18))

- Bind PyPI trusted publishing to named environments
  ([#1119](https://github.com/n24q02m/telegram/pull/1119),
  [`db951a3`](https://github.com/n24q02m/telegram/commit/db951a3764340b29226bdd3a207233b5787578cf))

- Migrate renovate config off deprecated options
  ([#1110](https://github.com/n24q02m/telegram/pull/1110),
  [`5b56fe8`](https://github.com/n24q02m/telegram/commit/5b56fe871f347ff773f70aaeaf0eac1ed77feb28))

- Point homepage at docs.n24q02m.com/servers/telegram/
  ([#1115](https://github.com/n24q02m/telegram/pull/1115),
  [`c79380b`](https://github.com/n24q02m/telegram/commit/c79380b432995235141fcb23a05a5362165952cd))

- Probe saved sessions in the data dir the server actually uses
  ([#1116](https://github.com/n24q02m/telegram/pull/1116),
  [`3f2b389`](https://github.com/n24q02m/telegram/commit/3f2b389fc4d3f0c51d297dde3531825fb150f6b1))

- **deps**: Bump pyjwt to 2.15.0 and virtualenv to 21.7.13
  ([#1107](https://github.com/n24q02m/telegram/pull/1107),
  [`cf54237`](https://github.com/n24q02m/telegram/commit/cf5423701b5868990d29e3b87be7dbeb2f960100))

- **deps**: Bump the uv group across 1 directory with 2 updates
  ([#1120](https://github.com/n24q02m/telegram/pull/1120),
  [`1942026`](https://github.com/n24q02m/telegram/commit/194202684b910fc7fb0bf92e40f43c64a520c4ea))

- **deps**: Bump virtualenv ([#1118](https://github.com/n24q02m/telegram/pull/1118),
  [`abc055d`](https://github.com/n24q02m/telegram/commit/abc055d519d7f7512767e506d81454f26dc83171))

### Features

- Make cd dispatch-only and add renovate minimum release age
  ([#1108](https://github.com/n24q02m/telegram/pull/1108),
  [`55c4e4d`](https://github.com/n24q02m/telegram/commit/55c4e4dd4d1a571d49a222a1af89773e36a7c362))

- Move telegram from mcp-core to hull core-py
  ([#1117](https://github.com/n24q02m/telegram/pull/1117),
  [`8cd0b6e`](https://github.com/n24q02m/telegram/commit/8cd0b6e0e867f99daa08b8a6ded7888671053cee))

- Remove cloudflare worker hosting surface ([#1113](https://github.com/n24q02m/telegram/pull/1113),
  [`6fcba3d`](https://github.com/n24q02m/telegram/commit/6fcba3d0c1faafcb71b07396704a3243a22626ed))

- Rename identity to telegram (PyPI n24q02m-telegram, image n24q02m/telegram)
  ([#1111](https://github.com/n24q02m/telegram/pull/1111),
  [`e1c5423`](https://github.com/n24q02m/telegram/commit/e1c54235430c98bc55d3ebb8c5668163d4075650))


## v4.22.0 (2026-09-13)

### Bug Fixes

- 🛡️ sentinel: prevent OOM DoS in bot_backend send_media
  ([#1100](https://github.com/n24q02m/better-telegram-mcp/pull/1100),
  [`60aa2d8`](https://github.com/n24q02m/better-telegram-mcp/commit/60aa2d83098e09f48acf19176304902b4096c429))

### Chores

- Bump mcp-core to 1.24.3 (backlog disposition pre-archive, user 2026-09-13)
  ([`44f9aa5`](https://github.com/n24q02m/better-telegram-mcp/commit/44f9aa5cbd7348496f299a63734845701761db6c))

### Documentation

- Add mode badge, install matrix, CD-managed deployment note
  ([#1103](https://github.com/n24q02m/better-telegram-mcp/pull/1103),
  [`b0cf9ea`](https://github.com/n24q02m/better-telegram-mcp/commit/b0cf9eab821a31f3d2fcf47504637870e18d2a22))

- Align mode badge with fleet standard (label 'mode', color 5C6BC0)
  ([`283bee4`](https://github.com/n24q02m/better-telegram-mcp/commit/283bee4d761cd48e4c7ca0a4efad403d7a9ae78f))

- Archival notice ([#1105](https://github.com/n24q02m/better-telegram-mcp/pull/1105),
  [`0a38130`](https://github.com/n24q02m/better-telegram-mcp/commit/0a381309d57821a4e2da8169f913c45821683dd0))

- Archival notice — repo no longer maintained (2026-09-13)
  ([#1105](https://github.com/n24q02m/better-telegram-mcp/pull/1105),
  [`0a38130`](https://github.com/n24q02m/better-telegram-mcp/commit/0a381309d57821a4e2da8169f913c45821683dd0))

- Move archival notice below tagline to keep registry metadata check green
  ([#1105](https://github.com/n24q02m/better-telegram-mcp/pull/1105),
  [`0a38130`](https://github.com/n24q02m/better-telegram-mcp/commit/0a381309d57821a4e2da8169f913c45821683dd0))

### Features

- 🎨 palette: prefer native labels for dynamic prompts
  ([#1101](https://github.com/n24q02m/better-telegram-mcp/pull/1101),
  [`618a1af`](https://github.com/n24q02m/better-telegram-mcp/commit/618a1afcb4568d90de7e431927ed387bf9de8377))


## v4.21.2 (2026-09-13)

### Bug Fixes

- Bump mcp-core to 1.24.1 ([#1097](https://github.com/n24q02m/better-telegram-mcp/pull/1097),
  [`80d4ac0`](https://github.com/n24q02m/better-telegram-mcp/commit/80d4ac02e28b80009738248d312a48a863b996ef))


## v4.21.1 (2026-09-12)

### Bug Fixes

- **deps**: Update @cloudflare/workers-types to ^5.20260905.1
  ([#1099](https://github.com/n24q02m/better-telegram-mcp/pull/1099),
  [`9a33cc8`](https://github.com/n24q02m/better-telegram-mcp/commit/9a33cc8a47c8e1606578e18eb486f75a200ecae0))


## v4.21.0 (2026-09-12)

### Chores

- Pin BSR action to v1.6.1 stable (6e688489)
  ([#1092](https://github.com/n24q02m/better-telegram-mcp/pull/1092),
  [`9a42ae9`](https://github.com/n24q02m/better-telegram-mcp/commit/9a42ae9a1c57237fd5e3540fc422fd7d5fb17038))

- **release**: Fix stale two-branch comment (single-main lane)
  ([`2953f32`](https://github.com/n24q02m/better-telegram-mcp/commit/2953f329cc59e3d53b9d2aa3115048a9713ea3ce))

- **release**: Single-main release lane (staging branch retired)
  ([`b4ea45d`](https://github.com/n24q02m/better-telegram-mcp/commit/b4ea45d5d507f1355bd7c879207d60dbab312553))

- **rulesets**: Align IaC with repo-bootstrap template
  ([`892948c`](https://github.com/n24q02m/better-telegram-mcp/commit/892948c739a5e93b1f5c8af7648e3346190da1c2))

### Features

- 🎨 palette: add dynamic form ux hierarchy
  ([#1095](https://github.com/n24q02m/better-telegram-mcp/pull/1095),
  [`e879d69`](https://github.com/n24q02m/better-telegram-mcp/commit/e879d697aeac5dea7197cb72df43177eb0a79041))


## v4.20.1 (2026-09-11)

### Bug Fixes

- **deps**: Update patch dependencies
  ([#1094](https://github.com/n24q02m/better-telegram-mcp/pull/1094),
  [`4355d96`](https://github.com/n24q02m/better-telegram-mcp/commit/4355d961461850674e7d6217350cf7cfe5b4555e))


## v4.20.0 (2026-09-11)

### Bug Fixes

- Bump mcp-core to 1.23.2 ([#1058](https://github.com/n24q02m/better-telegram-mcp/pull/1058),
  [`531b2ab`](https://github.com/n24q02m/better-telegram-mcp/commit/531b2abea5390bac1579d4da787495446ba32cc1))

- Clarify local Telegram install default
  ([`98ac785`](https://github.com/n24q02m/better-telegram-mcp/commit/98ac7853cd5276699f1f222f9f1a54199000678a))

- **deps**: Lock file maintenance
  ([#1090](https://github.com/n24q02m/better-telegram-mcp/pull/1090),
  [`4156b33`](https://github.com/n24q02m/better-telegram-mcp/commit/4156b3364ee4b35bd28ca6e39fb281d6b0524efe))

- **deps**: Lock file maintenance
  ([#1085](https://github.com/n24q02m/better-telegram-mcp/pull/1085),
  [`a6ea8ef`](https://github.com/n24q02m/better-telegram-mcp/commit/a6ea8ef6f607f569136436aa307e31f5f7a3549e))

- **deps**: Lock file maintenance
  ([#1079](https://github.com/n24q02m/better-telegram-mcp/pull/1079),
  [`4f12571`](https://github.com/n24q02m/better-telegram-mcp/commit/4f125715407533b00ec271a58d67c3b7a0f26161))

- **deps**: Lock file maintenance
  ([#1076](https://github.com/n24q02m/better-telegram-mcp/pull/1076),
  [`a460887`](https://github.com/n24q02m/better-telegram-mcp/commit/a460887f24ef293cbe0abe186307aa0c4f5df469))

- **deps**: Lock file maintenance
  ([#1072](https://github.com/n24q02m/better-telegram-mcp/pull/1072),
  [`0a74ff1`](https://github.com/n24q02m/better-telegram-mcp/commit/0a74ff1ca52f8e0163617a7e6476001d6afc7296))

- **deps**: Lock file maintenance
  ([#1065](https://github.com/n24q02m/better-telegram-mcp/pull/1065),
  [`785e261`](https://github.com/n24q02m/better-telegram-mcp/commit/785e2615f1231bacd477021f53f5cbf7c392502e))

- **deps**: Lock file maintenance
  ([#1062](https://github.com/n24q02m/better-telegram-mcp/pull/1062),
  [`4684374`](https://github.com/n24q02m/better-telegram-mcp/commit/46843746e33a0ced16c80687999fe16b6d143442))

- **deps**: Update @cloudflare/workers-types to ^5.20260828.1
  ([#1071](https://github.com/n24q02m/better-telegram-mcp/pull/1071),
  [`c6ae360`](https://github.com/n24q02m/better-telegram-mcp/commit/c6ae3604b419322edd9d61a1cf9dd5bd6c86be23))

- **deps**: Update @cloudflare/workers-types to ^5.20260830.1
  ([#1078](https://github.com/n24q02m/better-telegram-mcp/pull/1078),
  [`84d05f1`](https://github.com/n24q02m/better-telegram-mcp/commit/84d05f171620ba85650d767929b2526f7a947277))

- **deps**: Update @cloudflare/workers-types to ^5.20260902.1
  ([#1089](https://github.com/n24q02m/better-telegram-mcp/pull/1089),
  [`078d579`](https://github.com/n24q02m/better-telegram-mcp/commit/078d57942f02ba8acb03ec82c925b6740c5c53a0))

- **deps**: Update dawidd6/action-send-mail action to v20
  ([#1084](https://github.com/n24q02m/better-telegram-mcp/pull/1084),
  [`c1bd733`](https://github.com/n24q02m/better-telegram-mcp/commit/c1bd733595a05ee5efd4df2a1bc9e6529b573a29))

- **deps**: Update n24q02m/better-semantic-release action to v1.6.0
  ([#1068](https://github.com/n24q02m/better-telegram-mcp/pull/1068),
  [`46d8ae0`](https://github.com/n24q02m/better-telegram-mcp/commit/46d8ae09c7592077054ea212ce319b74dd22a34a))

- **deps**: Update patch dependencies
  ([#1083](https://github.com/n24q02m/better-telegram-mcp/pull/1083),
  [`79840bd`](https://github.com/n24q02m/better-telegram-mcp/commit/79840bd3a3fadaff9e4a9f7f86db29c9614114aa))

- **deps**: Update patch dependencies
  ([#1075](https://github.com/n24q02m/better-telegram-mcp/pull/1075),
  [`dc954c9`](https://github.com/n24q02m/better-telegram-mcp/commit/dc954c993edfa81f55f20add3cd9ad039dec8ef2))

- **deps**: Update patch dependencies
  ([#1070](https://github.com/n24q02m/better-telegram-mcp/pull/1070),
  [`f032ef4`](https://github.com/n24q02m/better-telegram-mcp/commit/f032ef43164b17b194926307a0511b3fbba400ba))

- **deps**: Update patch dependencies
  ([#1067](https://github.com/n24q02m/better-telegram-mcp/pull/1067),
  [`5c91d35`](https://github.com/n24q02m/better-telegram-mcp/commit/5c91d3590a88621b17c100fc7b026384ce698624))

- **deps**: Update patch dependencies
  ([#1064](https://github.com/n24q02m/better-telegram-mcp/pull/1064),
  [`d300b99`](https://github.com/n24q02m/better-telegram-mcp/commit/d300b99a1cf9ba1b6b0a6816aedd282459d09776))

- **deps**: Update patch dependencies
  ([#1061](https://github.com/n24q02m/better-telegram-mcp/pull/1061),
  [`db71878`](https://github.com/n24q02m/better-telegram-mcp/commit/db718784fff0d0fb9c470d9c946e736031e67012))

- **deps**: Update python:3.13-slim-bookworm Docker digest to ed86c82
  ([#1060](https://github.com/n24q02m/better-telegram-mcp/pull/1060),
  [`e41989e`](https://github.com/n24q02m/better-telegram-mcp/commit/e41989e8022107e8ac099b0ba275e6a662b4a246))

### Continuous Integration

- Wire unified merge=release ladder (push staging=beta, main=stable)
  ([`aea8abe`](https://github.com/n24q02m/better-telegram-mcp/commit/aea8abede3c9ee1771243352fbda4444303733b7))

### Features

- Harden Telegram auth cleanup and relay form
  ([`f9d130c`](https://github.com/n24q02m/better-telegram-mcp/commit/f9d130c8e98ae6dbdcc433ce6db852b18f97f9b1))

- 🎨 palette: server error validation feedback
  ([#1059](https://github.com/n24q02m/better-telegram-mcp/pull/1059),
  [`25a9acb`](https://github.com/n24q02m/better-telegram-mcp/commit/25a9acbe96ed9524d6c79abb4cd9ed45d30c1a93))

- 🎨 palette: smooth view transitions
  ([#1066](https://github.com/n24q02m/better-telegram-mcp/pull/1066),
  [`a315709`](https://github.com/n24q02m/better-telegram-mcp/commit/a315709836abb7f16a30b7182d61d5bd1932a5dc))


## v4.19.0 (2026-08-31)


## v4.19.0-beta.1 (2026-08-31)

### Bug Fixes

- Repair MCP registry publication
  ([`6c58f9a`](https://github.com/n24q02m/better-telegram-mcp/commit/6c58f9a1aaef9bc2ce64c4cb1caee1580afd6a44))

- **deps**: Bump better-semantic-release to v1.5.0
  ([`be5b930`](https://github.com/n24q02m/better-telegram-mcp/commit/be5b93008aa611644f678ee251e33f08676d0938))

- **deps**: Lock file maintenance
  ([#1055](https://github.com/n24q02m/better-telegram-mcp/pull/1055),
  [`6b5bab7`](https://github.com/n24q02m/better-telegram-mcp/commit/6b5bab7442beea11ce884a3f628054052e306b12))

- **deps**: Lock file maintenance
  ([#1051](https://github.com/n24q02m/better-telegram-mcp/pull/1051),
  [`4e7d137`](https://github.com/n24q02m/better-telegram-mcp/commit/4e7d13734ba7d2330318a7bf8ac7529d466fd4ff))

- **deps**: Update @cloudflare/workers-types to ^5.20260823.1
  ([#1054](https://github.com/n24q02m/better-telegram-mcp/pull/1054),
  [`569fa8e`](https://github.com/n24q02m/better-telegram-mcp/commit/569fa8ed3498854517f70adbfbbd88078cd82429))

- **deps**: Update patch dependencies
  ([#1049](https://github.com/n24q02m/better-telegram-mcp/pull/1049),
  [`b1724da`](https://github.com/n24q02m/better-telegram-mcp/commit/b1724da34f516943a8bfd24ad822f96a37060714))

### Features

- Clarify disabled password toggle state
  ([`6359f6a`](https://github.com/n24q02m/better-telegram-mcp/commit/6359f6a4238557eda6e3503e3a0f370d45e9c334))

- 🎨 palette: add dual-channel validation feedback (shake animation)
  ([#1056](https://github.com/n24q02m/better-telegram-mcp/pull/1056),
  [`f00d026`](https://github.com/n24q02m/better-telegram-mcp/commit/f00d0265a21d73c1e45feaefea173c20afc69761))


## v4.18.0 (2026-08-29)

### Bug Fixes

- 🛡️ sentinel: prevent OOM DoS by limiting local file sizes in user_backend send_media
  ([#1046](https://github.com/n24q02m/better-telegram-mcp/pull/1046),
  [`252cdb8`](https://github.com/n24q02m/better-telegram-mcp/commit/252cdb876c733031d4e8928d45541e5ad8221cbc))

- **deps**: Lock file maintenance
  ([#1047](https://github.com/n24q02m/better-telegram-mcp/pull/1047),
  [`db7ff53`](https://github.com/n24q02m/better-telegram-mcp/commit/db7ff53fb02a230511947642a72ccdc00ab4409e))

- **deps**: Update non-major dev dependencies
  ([#1044](https://github.com/n24q02m/better-telegram-mcp/pull/1044),
  [`274dbfe`](https://github.com/n24q02m/better-telegram-mcp/commit/274dbfe64f98dd3aeddb30a730e9652cfa2646ad))

- **deps**: Update patch dependencies
  ([#1043](https://github.com/n24q02m/better-telegram-mcp/pull/1043),
  [`7bc74f8`](https://github.com/n24q02m/better-telegram-mcp/commit/7bc74f887b09167c5981aacb6f8d022d00a9ede7))

- **deps**: Update python:3.13-slim-bookworm Docker digest to c45a22e
  ([`fadb62f`](https://github.com/n24q02m/better-telegram-mcp/commit/fadb62fb6ff0f92938c17061da5cbeb376f92e49))

### Chores

- Bump better-semantic-release to v1.4.0
  ([#1038](https://github.com/n24q02m/better-telegram-mcp/pull/1038),
  [`c0281a6`](https://github.com/n24q02m/better-telegram-mcp/commit/c0281a6be624622a5ff38f0bb5d8c71750337a13))

### Documentation

- **telegram**: Clarify credential renderer ownership
  ([#1040](https://github.com/n24q02m/better-telegram-mcp/pull/1040),
  [`e7684c2`](https://github.com/n24q02m/better-telegram-mcp/commit/e7684c234c8aac422f9a6c2b9c49f1d37c15f9cc))

### Features

- 🎨 palette: add dynamic password visibility toggle
  ([#1040](https://github.com/n24q02m/better-telegram-mcp/pull/1040),
  [`e7684c2`](https://github.com/n24q02m/better-telegram-mcp/commit/e7684c234c8aac422f9a6c2b9c49f1d37c15f9cc))

### Testing

- Cover user backend media size guards
  ([#1046](https://github.com/n24q02m/better-telegram-mcp/pull/1046),
  [`252cdb8`](https://github.com/n24q02m/better-telegram-mcp/commit/252cdb876c733031d4e8928d45541e5ad8221cbc))

- **telegram**: Cover password toggle state
  ([#1040](https://github.com/n24q02m/better-telegram-mcp/pull/1040),
  [`e7684c2`](https://github.com/n24q02m/better-telegram-mcp/commit/e7684c234c8aac422f9a6c2b9c49f1d37c15f9cc))


## v4.18.0-beta.6 (2026-08-24)

### Bug Fixes

- **deps**: Update actions/setup-node action to v7
  ([#1014](https://github.com/n24q02m/better-telegram-mcp/pull/1014),
  [`079d601`](https://github.com/n24q02m/better-telegram-mcp/commit/079d601a47fba4e74893097496b96f627bf04f9a))

- **deps**: Update actions/setup-python action to v7
  ([#1015](https://github.com/n24q02m/better-telegram-mcp/pull/1015),
  [`4fc5c50`](https://github.com/n24q02m/better-telegram-mcp/commit/4fc5c508a893e8e80ce1073f339178ad77f8c1e5))

### Features

- ⚡ bolt: o(1) existence checks ([#1031](https://github.com/n24q02m/better-telegram-mcp/pull/1031),
  [`b099582`](https://github.com/n24q02m/better-telegram-mcp/commit/b099582bbb8abbc27373672c8b47213b181ff33f))


## v4.18.0-beta.5 (2026-08-24)

### Bug Fixes

- Remove retired Telegram host claim
  ([#1035](https://github.com/n24q02m/better-telegram-mcp/pull/1035),
  [`86eec8d`](https://github.com/n24q02m/better-telegram-mcp/commit/86eec8db80a3d122ca753399b6ffa2864f157e19))

### Features

- Expose forum topic_id in serialized messages
  ([#1036](https://github.com/n24q02m/better-telegram-mcp/pull/1036),
  [`d9586cb`](https://github.com/n24q02m/better-telegram-mcp/commit/d9586cbe33711b2a6a110cb806ab008678596575))

- 🎨 palette: visually unambiguous disabled state for password toggle
  ([#1030](https://github.com/n24q02m/better-telegram-mcp/pull/1030),
  [`34c223a`](https://github.com/n24q02m/better-telegram-mcp/commit/34c223a5f2200953698811c36c703afa8e188a5e))


## v4.18.0-beta.4 (2026-08-24)

### Bug Fixes

- **deps**: Prevent pydantic settings startup warning
  ([#1034](https://github.com/n24q02m/better-telegram-mcp/pull/1034),
  [`764c134`](https://github.com/n24q02m/better-telegram-mcp/commit/764c134837cb24253f915dc5c2c532afe1438411))


## v4.18.0-beta.3 (2026-08-24)

### Bug Fixes

- Pin workflow actions ([#1029](https://github.com/n24q02m/better-telegram-mcp/pull/1029),
  [`d175c6f`](https://github.com/n24q02m/better-telegram-mcp/commit/d175c6f0d682249364bdcfad7862ca4f45c93e16))

- **deps**: Keep MCP 1 compatibility boundary
  ([#1012](https://github.com/n24q02m/better-telegram-mcp/pull/1012),
  [`4416ef0`](https://github.com/n24q02m/better-telegram-mcp/commit/4416ef0bda973ba8fb0d881f96a6010dedc53149))

- **deps**: Update minor dependencies
  ([#1012](https://github.com/n24q02m/better-telegram-mcp/pull/1012),
  [`4416ef0`](https://github.com/n24q02m/better-telegram-mcp/commit/4416ef0bda973ba8fb0d881f96a6010dedc53149))


## v4.18.0-beta.2 (2026-08-24)

### Bug Fixes

- Accept dehost tombstone canary ([#1033](https://github.com/n24q02m/better-telegram-mcp/pull/1033),
  [`096f0da`](https://github.com/n24q02m/better-telegram-mcp/commit/096f0da86a8ba83d61b86c5c97879b92ab95ff61))


## v4.18.0-beta.1 (2026-08-24)

### Bug Fixes

- Derive the tilde-traversal depth from the real home
  ([#975](https://github.com/n24q02m/better-telegram-mcp/pull/975),
  [`e4f61ec`](https://github.com/n24q02m/better-telegram-mcp/commit/e4f61ec4633cfc6d601ff21e4774995247c4c725))

- Describe the HTTP mode instead of advertising a personal instance
  ([`8f42d52`](https://github.com/n24q02m/better-telegram-mcp/commit/8f42d52efb7b2a85d6a20f6097bdbdd096fbe2b0))

- Drop code_quality from the main ruleset
  ([#958](https://github.com/n24q02m/better-telegram-mcp/pull/958),
  [`1ef1ea2`](https://github.com/n24q02m/better-telegram-mcp/commit/1ef1ea2716adc686c7d9aa862ec7bc6fcac18e0f))

- Drop rangeStrategy from update-type package rules
  ([#956](https://github.com/n24q02m/better-telegram-mcp/pull/956),
  [`da37457`](https://github.com/n24q02m/better-telegram-mcp/commit/da37457208ad81a2bfe1a69ce05d6f7e6e158763))

- Isolate test HOME so per-plugin stores cannot reach the real home
  ([#975](https://github.com/n24q02m/better-telegram-mcp/pull/975),
  [`e4f61ec`](https://github.com/n24q02m/better-telegram-mcp/commit/e4f61ec4633cfc6d601ff21e4774995247c4c725))

- Move this repo to Apache-2.0 ([#973](https://github.com/n24q02m/better-telegram-mcp/pull/973),
  [`5a630fe`](https://github.com/n24q02m/better-telegram-mcp/commit/5a630fe0e5860a1e627a1557cabdbec56bd0e9c8))

- Offload blocking Telegram I/O to worker threads
  ([`2e04e07`](https://github.com/n24q02m/better-telegram-mcp/commit/2e04e074fa08f8c8c56ec0bc4d46971fe7ebc7e6))

- Pin GitHub Action references to commit SHAs
  ([#954](https://github.com/n24q02m/better-telegram-mcp/pull/954),
  [`a7a7ac4`](https://github.com/n24q02m/better-telegram-mcp/commit/a7a7ac4d12f250ed76587ac1e7d56d8982281b21))

- Pin HOME in the tilde-traversal security tests
  ([#975](https://github.com/n24q02m/better-telegram-mcp/pull/975),
  [`e4f61ec`](https://github.com/n24q02m/better-telegram-mcp/commit/e4f61ec4633cfc6d601ff21e4774995247c4c725))

- Preserve session index consistency
  ([#1006](https://github.com/n24q02m/better-telegram-mcp/pull/1006),
  [`c127816`](https://github.com/n24q02m/better-telegram-mcp/commit/c1278169ba8bcb1995551f2f307f352e314915b1))

- Prevent OOM in bot media uploads
  ([`8e985c2`](https://github.com/n24q02m/better-telegram-mcp/commit/8e985c23a848d2518a727a4a7bea285955ebaa75))

- Remove redundant orphan-tag shell guard (better-semantic-release @v1 has a built-in one)
  ([#953](https://github.com/n24q02m/better-telegram-mcp/pull/953),
  [`626f0b0`](https://github.com/n24q02m/better-telegram-mcp/commit/626f0b099307ef178fdc2dc65788a27feb954436))

- Respect managed CodeQL setup ([#1008](https://github.com/n24q02m/better-telegram-mcp/pull/1008),
  [`84d25c3`](https://github.com/n24q02m/better-telegram-mcp/commit/84d25c360677a52e313beffc03b937135f965c29))

- Stop the home-isolation guard from polluting the real store when it fires
  ([#975](https://github.com/n24q02m/better-telegram-mcp/pull/975),
  [`e4f61ec`](https://github.com/n24q02m/better-telegram-mcp/commit/e4f61ec4633cfc6d601ff21e4774995247c4c725))

- **deps**: Bump mcp-core to 1.23.0
  ([#1010](https://github.com/n24q02m/better-telegram-mcp/pull/1010),
  [`9dff895`](https://github.com/n24q02m/better-telegram-mcp/commit/9dff8958c29fcb4663e2a50fd149019c29f2cb69))

- **deps**: Remediate postcss security alert
  ([#1009](https://github.com/n24q02m/better-telegram-mcp/pull/1009),
  [`e11f36d`](https://github.com/n24q02m/better-telegram-mcp/commit/e11f36d5ce26ccf5490aaf5054a62bc06a5b71b1))

- **deps**: Update @cloudflare/workers-types to ^5.20260809.1
  ([#1019](https://github.com/n24q02m/better-telegram-mcp/pull/1019),
  [`2470f80`](https://github.com/n24q02m/better-telegram-mcp/commit/2470f80ee9a1ab9cdc12ae5942e2d1e546df10d1))

- **deps**: Update cryptography to v50 [SECURITY]
  ([#984](https://github.com/n24q02m/better-telegram-mcp/pull/984),
  [`3be7c4c`](https://github.com/n24q02m/better-telegram-mcp/commit/3be7c4cb6768b7075ae6c20d6df88b988223ded9))

- **deps**: Update dependency uvicorn to >=0.51.0
  ([#911](https://github.com/n24q02m/better-telegram-mcp/pull/911),
  [`7203301`](https://github.com/n24q02m/better-telegram-mcp/commit/7203301455fecaf16396292a15d8d25bd72b053f))

- **deps**: Update patch dependencies
  ([#1011](https://github.com/n24q02m/better-telegram-mcp/pull/1011),
  [`fa196d2`](https://github.com/n24q02m/better-telegram-mcp/commit/fa196d2b65cb96d27e5c63518c4039115847c6fb))

- **deps**: Update python:3.13-slim-bookworm Docker digest to 00faa2d
  ([#935](https://github.com/n24q02m/better-telegram-mcp/pull/935),
  [`d258458`](https://github.com/n24q02m/better-telegram-mcp/commit/d258458c90caedaafcc1b2e1dd90c8f25ab94333))

- **deps**: Update ruff to >=0.16.2
  ([#1013](https://github.com/n24q02m/better-telegram-mcp/pull/1013),
  [`37837de`](https://github.com/n24q02m/better-telegram-mcp/commit/37837de3a7eb5efc9acb495a1fe93d1b7cc5675c))

- **deps**: Update typescript to v7
  ([#920](https://github.com/n24q02m/better-telegram-mcp/pull/920),
  [`3af74ad`](https://github.com/n24q02m/better-telegram-mcp/commit/3af74ad385070bd45a343b6219c72b0a58bb6c59))

- **telegram**: Align bot auth and e2e coverage
  ([#1004](https://github.com/n24q02m/better-telegram-mcp/pull/1004),
  [`04e7f98`](https://github.com/n24q02m/better-telegram-mcp/commit/04e7f98fc40bec7ffde0d54fdc9314118d0a6787))

### Chores

- **deps**: Bump sharp in the npm_and_yarn group across 1 directory
  ([#980](https://github.com/n24q02m/better-telegram-mcp/pull/980),
  [`5b8b1e4`](https://github.com/n24q02m/better-telegram-mcp/commit/5b8b1e4303e6c7b37f7dffb24d9058902b613f2f))

### Features

- Add hosted runtime tombstone ([#1032](https://github.com/n24q02m/better-telegram-mcp/pull/1032),
  [`f02ddb5`](https://github.com/n24q02m/better-telegram-mcp/commit/f02ddb503a9215483dc974fbf72be299377f2ebe))

- Apply repository bootstrap standards
  ([#1008](https://github.com/n24q02m/better-telegram-mcp/pull/1008),
  [`84d25c3`](https://github.com/n24q02m/better-telegram-mcp/commit/84d25c360677a52e313beffc03b937135f965c29))

- Derive a stable subject from the workspace username
  ([#955](https://github.com/n24q02m/better-telegram-mcp/pull/955),
  [`dcaf609`](https://github.com/n24q02m/better-telegram-mcp/commit/dcaf609a258e422772e2b718ab17d4cd6a51a5c4))

- Sync cross-promo section ([#963](https://github.com/n24q02m/better-telegram-mcp/pull/963),
  [`99912ed`](https://github.com/n24q02m/better-telegram-mcp/commit/99912ed66591aff4845fa8e1ea25b22eaab6a473))

- ⚡ bolt: o(1) existence checks ([#1006](https://github.com/n24q02m/better-telegram-mcp/pull/1006),
  [`c127816`](https://github.com/n24q02m/better-telegram-mcp/commit/c1278169ba8bcb1995551f2f307f352e314915b1))

- 🎨 palette: add password visibility toggle to bot token field
  ([#1007](https://github.com/n24q02m/better-telegram-mcp/pull/1007),
  [`d8c09cd`](https://github.com/n24q02m/better-telegram-mcp/commit/d8c09cd446936a32f2f49227899c6528420b60d4))


## v4.17.0 (2026-07-18)


## v4.17.0-beta.1 (2026-07-18)

### Bug Fixes

- Add orphan-tag integrity guard to release CI
  ([#944](https://github.com/n24q02m/better-telegram-mcp/pull/944),
  [`75bac8d`](https://github.com/n24q02m/better-telegram-mcp/commit/75bac8d5b8a358c74ce4beb40522b3e3aeb1ea91))

- Adopt better-semantic-release for built-in release guards
  ([`56e65be`](https://github.com/n24q02m/better-telegram-mcp/commit/56e65be364f399e9772b18ec914a31d916e0c719))

- Bump mcp-core floor to 1.19.0 stable
  ([#942](https://github.com/n24q02m/better-telegram-mcp/pull/942),
  [`2b2f0ef`](https://github.com/n24q02m/better-telegram-mcp/commit/2b2f0efbe38c041dde849b719ea7da63a78b2bf2))

- Clear error when getFile response lacks file_path
  ([#941](https://github.com/n24q02m/better-telegram-mcp/pull/941),
  [`2ecdb3f`](https://github.com/n24q02m/better-telegram-mcp/commit/2ecdb3f9964c279e6fce4a159bc29f840732cb15))

- Load credentials without os.environ mutation
  ([#947](https://github.com/n24q02m/better-telegram-mcp/pull/947),
  [`6abdd89`](https://github.com/n24q02m/better-telegram-mcp/commit/6abdd89c24d15dc0388080d28a4cdaae77f33eb0))

- Pin rangeStrategy on delayed packageRules to fix renovate artifacts failure
  ([#945](https://github.com/n24q02m/better-telegram-mcp/pull/945),
  [`c8910da`](https://github.com/n24q02m/better-telegram-mcp/commit/c8910da245b83982e7d90a8d5b9cc5b01da3ffb9))

- Stream media downloads with 50MB size cap to prevent OOM
  ([`a999622`](https://github.com/n24q02m/better-telegram-mcp/commit/a999622fcf60156796e9396f4274df06a841595e))

- Unify single-user credential storage onto PerPluginStore
  ([#949](https://github.com/n24q02m/better-telegram-mcp/pull/949),
  [`950a4b2`](https://github.com/n24q02m/better-telegram-mcp/commit/950a4b213eb87b9e22f3e9ca8cb41c234ce6c4fa))

### Features

- Accept generic key/value form for config set
  ([#950](https://github.com/n24q02m/better-telegram-mcp/pull/950),
  [`00db1ab`](https://github.com/n24q02m/better-telegram-mcp/commit/00db1ab9d892647d3c9fca373320c8dd37bd7c35))

- Add auth subcommand as the standard alias of login
  ([#950](https://github.com/n24q02m/better-telegram-mcp/pull/950),
  [`00db1ab`](https://github.com/n24q02m/better-telegram-mcp/commit/00db1ab9d892647d3c9fca373320c8dd37bd7c35))

- Add PR-title conventional-commit gate + no-bump release warning
  ([#948](https://github.com/n24q02m/better-telegram-mcp/pull/948),
  [`8e68111`](https://github.com/n24q02m/better-telegram-mcp/commit/8e68111d93fba71387767a9be7e2de713dde19e7))

- Config set key/value parity + auth subcommand alias
  ([#950](https://github.com/n24q02m/better-telegram-mcp/pull/950),
  [`00db1ab`](https://github.com/n24q02m/better-telegram-mcp/commit/00db1ab9d892647d3c9fca373320c8dd37bd7c35))

- Document CLI, smithery, and self-host endpoint in README
  ([#938](https://github.com/n24q02m/better-telegram-mcp/pull/938),
  [`4882eab`](https://github.com/n24q02m/better-telegram-mcp/commit/4882eab36751b0813d73e99c059091fce2cae1fb))

- Use core credential form renderer with tabs schema, drop fork
  ([#943](https://github.com/n24q02m/better-telegram-mcp/pull/943),
  [`9fef7cc`](https://github.com/n24q02m/better-telegram-mcp/commit/9fef7cc58cd23b68b8b4208954a7af038c0910d8))


## v4.16.0 (2026-07-14)

### Bug Fixes

- **deps**: Lock file maintenance ([#931](https://github.com/n24q02m/better-telegram-mcp/pull/931),
  [`4505561`](https://github.com/n24q02m/better-telegram-mcp/commit/4505561c56cbb34c0d0b317dd84a0867ce5b63d9))

### Features

- Add smithery.yaml for stdio deployment
  ([#933](https://github.com/n24q02m/better-telegram-mcp/pull/933),
  [`74acd75`](https://github.com/n24q02m/better-telegram-mcp/commit/74acd753a8a5e0a75c8d89f7e2b8b63d8124b317))


## v4.16.0-beta.7 (2026-07-13)

### Bug Fixes

- Correct mention gate expression (balanced parens + precedence)
  ([#929](https://github.com/n24q02m/better-telegram-mcp/pull/929),
  [`3d7e5cf`](https://github.com/n24q02m/better-telegram-mcp/commit/3d7e5cfa3edefddc0ca4f1d9aeb805a2fa349026))

- Gate oc mention job on comment author write access
  ([#929](https://github.com/n24q02m/better-telegram-mcp/pull/929),
  [`3d7e5cf`](https://github.com/n24q02m/better-telegram-mcp/commit/3d7e5cfa3edefddc0ca4f1d9aeb805a2fa349026))

- Give bot-mode download_media a real path via getFile
  ([#930](https://github.com/n24q02m/better-telegram-mcp/pull/930),
  [`2722120`](https://github.com/n24q02m/better-telegram-mcp/commit/2722120796e5638031b8de986dbcdf8bd18a0a91))

- Redact bot token in download_media file-GET error path
  ([#930](https://github.com/n24q02m/better-telegram-mcp/pull/930),
  [`2722120`](https://github.com/n24q02m/better-telegram-mcp/commit/2722120796e5638031b8de986dbcdf8bd18a0a91))

- Run opencode bot on hosted runners
  ([#928](https://github.com/n24q02m/better-telegram-mcp/pull/928),
  [`fef22a0`](https://github.com/n24q02m/better-telegram-mcp/commit/fef22a046b6a7744a8b450f31e219865b262166a))


## v4.16.0-beta.6 (2026-07-13)

### Bug Fixes

- Add XPIA defense wrapper for external Telegram content
  ([#927](https://github.com/n24q02m/better-telegram-mcp/pull/927),
  [`fd74595`](https://github.com/n24q02m/better-telegram-mcp/commit/fd74595bfd478a49d3fe1c5e3694cf11a2ad03bc))

- **deps**: Lock file maintenance ([#924](https://github.com/n24q02m/better-telegram-mcp/pull/924),
  [`e05b72d`](https://github.com/n24q02m/better-telegram-mcp/commit/e05b72d88a9655670fc4dc8783eb0a058f7dc23d))

- **deps**: Lock file maintenance ([#922](https://github.com/n24q02m/better-telegram-mcp/pull/922),
  [`e938fe8`](https://github.com/n24q02m/better-telegram-mcp/commit/e938fe8963cbf30c1e2311f129da879534d5134b))

- **deps**: Lock file maintenance ([#921](https://github.com/n24q02m/better-telegram-mcp/pull/921),
  [`56a6b06`](https://github.com/n24q02m/better-telegram-mcp/commit/56a6b06126229045ad37ebf3f2c243f3b250d132))


## v4.16.0-beta.5 (2026-07-11)

### Features

- Return structured content from domain tools
  ([#918](https://github.com/n24q02m/better-telegram-mcp/pull/918),
  [`44daf4a`](https://github.com/n24q02m/better-telegram-mcp/commit/44daf4a28731782b67bfe67cb784029152b21885))


## v4.16.0-beta.4 (2026-07-11)

### Bug Fixes

- Bump mcp-core floor to 1.19.0b4 ([#917](https://github.com/n24q02m/better-telegram-mcp/pull/917),
  [`af82098`](https://github.com/n24q02m/better-telegram-mcp/commit/af82098e6fedae3b2bc1e2b3cc5593005bb6f428))

### Features

- Cli login/logout with api identity marker and credential-state stdio gate
  ([#917](https://github.com/n24q02m/better-telegram-mcp/pull/917),
  [`af82098`](https://github.com/n24q02m/better-telegram-mcp/commit/af82098e6fedae3b2bc1e2b3cc5593005bb6f428))

- Mount shared cli builder with login/logout subcommands
  ([#917](https://github.com/n24q02m/better-telegram-mcp/pull/917),
  [`af82098`](https://github.com/n24q02m/better-telegram-mcp/commit/af82098e6fedae3b2bc1e2b3cc5593005bb6f428))

- Relax stdio gate to credential state and warn on api identity change
  ([#917](https://github.com/n24q02m/better-telegram-mcp/pull/917),
  [`af82098`](https://github.com/n24q02m/better-telegram-mcp/commit/af82098e6fedae3b2bc1e2b3cc5593005bb6f428))


## v4.16.0-beta.3 (2026-07-11)

### Bug Fixes

- Block SSRF bypass via IPv6 unspecified address
  ([`e636718`](https://github.com/n24q02m/better-telegram-mcp/commit/e6367187cf7643982b3deb7b0e04b1592d80231a))

- Bump @cloudflare/workers-types to v5
  ([#908](https://github.com/n24q02m/better-telegram-mcp/pull/908),
  [`dc027c0`](https://github.com/n24q02m/better-telegram-mcp/commit/dc027c07c21ad01b4ec41671feee25916d12ba03))

- Bump mcp-core floor to 1.19.0b2 ([#916](https://github.com/n24q02m/better-telegram-mcp/pull/916),
  [`cf88205`](https://github.com/n24q02m/better-telegram-mcp/commit/cf882057a5a1042d453d638ecd268cf3e620f88a))

- Bump n24q02m-mcp-core to 1.18.2 ([#907](https://github.com/n24q02m/better-telegram-mcp/pull/907),
  [`eceb6be`](https://github.com/n24q02m/better-telegram-mcp/commit/eceb6be969a5a460eaa4ab505e97b0a375004686))

- Cache dynamic backend import in get_backend hot path
  ([`abee7da`](https://github.com/n24q02m/better-telegram-mcp/commit/abee7da9d1cc0f258f97174003b01cada166044c))

- Disable password toggles during form submission
  ([`cbc8614`](https://github.com/n24q02m/better-telegram-mcp/commit/cbc8614b9081321b404d1784d3b570c6293f2cbb))

- Document public-by-design identifiers for secret scanners
  ([#905](https://github.com/n24q02m/better-telegram-mcp/pull/905),
  [`960855c`](https://github.com/n24q02m/better-telegram-mcp/commit/960855ce8d59fcace86ada5100c0efc8bbdaf927))

- Enforce fix(deps) semantic commit prefix in renovate config
  ([`a893e56`](https://github.com/n24q02m/better-telegram-mcp/commit/a893e5636b852d67aad6a85d3d2d967418823e71))

- Ensure dual-channel validation feedback on server errors
  ([`083e553`](https://github.com/n24q02m/better-telegram-mcp/commit/083e5537bb899f6799793a6f8fef0d0e78d350d7))

- Lock file maintenance
  ([`695a114`](https://github.com/n24q02m/better-telegram-mcp/commit/695a11446981b460014f49baf7d5ca646d45371d))

- Make renovate automerge effective (isolated groups, digest+lockfile automerge, 7-day cooldown)
  ([`23e56b3`](https://github.com/n24q02m/better-telegram-mcp/commit/23e56b3bf35c77eb0f45128d061d1edc3b0c8aa2))

- Parallelize pending OTP cleanup and skip redundant KV writes
  ([`cf76497`](https://github.com/n24q02m/better-telegram-mcp/commit/cf764970d6f1c60ce9291a6d76e1e0776814ab09))

- Repair worker test types and gate CI on tsc --noEmit
  ([`cf29efe`](https://github.com/n24q02m/better-telegram-mcp/commit/cf29efecbd72569ffd9593a0bdf4d5e634a76d8f))

- Sync aria-label when resetting password toggle
  ([`c4293e8`](https://github.com/n24q02m/better-telegram-mcp/commit/c4293e878b452092088713f17f1453d06a355ffc))

### Chores

- **deps**: Update astral-sh/setup-uv action to v8.3.2
  ([#912](https://github.com/n24q02m/better-telegram-mcp/pull/912),
  [`dd89f1d`](https://github.com/n24q02m/better-telegram-mcp/commit/dd89f1db1a510305780798f7fb6fe5b46bfa8f5e))

### Features

- Resolve telegram api identity via bundled client BYO chain
  ([#916](https://github.com/n24q02m/better-telegram-mcp/pull/916),
  [`cf88205`](https://github.com/n24q02m/better-telegram-mcp/commit/cf882057a5a1042d453d638ecd268cf3e620f88a))


## v4.16.0-beta.2 (2026-07-10)

### Bug Fixes

- Decline standing GET /mcp SSE stream at the edge
  ([#904](https://github.com/n24q02m/better-telegram-mcp/pull/904),
  [`52d88cf`](https://github.com/n24q02m/better-telegram-mcp/commit/52d88cf75e903ac99283df0f1883d29ae1623f8c))

- Fail the release when the computed version already exists on PyPI
  ([#903](https://github.com/n24q02m/better-telegram-mcp/pull/903),
  [`6c5e2ac`](https://github.com/n24q02m/better-telegram-mcp/commit/6c5e2acdc0772b31b6c57f30a26bff2a0bcfdeab))


## v4.16.0-beta.1 (2026-07-10)

### Bug Fixes

- Reject unauthenticated /mcp at the Worker edge
  ([#902](https://github.com/n24q02m/better-telegram-mcp/pull/902),
  [`42e8d76`](https://github.com/n24q02m/better-telegram-mcp/commit/42e8d76c5f48ff576c7b6ff758203ad6dc47d114))

### Features

- Add opencode github agent (responds to /oc)
  ([`bc2a718`](https://github.com/n24q02m/better-telegram-mcp/commit/bc2a71840620374478915cb04dfb0d6582971ead))

- Add review-learnings store the automated reviewer must obey
  ([`284e406`](https://github.com/n24q02m/better-telegram-mcp/commit/284e406b63471b5cadcaac7d777cddbbe1691512))

- Auto-respond only to issues and PRs opened by outside people
  ([`4d0b28c`](https://github.com/n24q02m/better-telegram-mcp/commit/4d0b28cf595f6ec831e3b639696848f9e82ea579))

- Reviewer must obey .github/review-learnings.md
  ([`4509e1b`](https://github.com/n24q02m/better-telegram-mcp/commit/4509e1ba34beac98319117137442147881031917))


## v4.15.0 (2026-07-05)


## v4.15.0-beta.1 (2026-07-05)

### Bug Fixes

- Guard PUBLIC_URL substitution on placeholder presence in cf-deploy.mjs
  ([#881](https://github.com/n24q02m/better-telegram-mcp/pull/881),
  [`daef308`](https://github.com/n24q02m/better-telegram-mcp/commit/daef308e8c4157200837e6b48c2662b7f470506b))

- Make Workers Paid plan prerequisite explicit for Containers in README
  ([#881](https://github.com/n24q02m/better-telegram-mcp/pull/881),
  [`daef308`](https://github.com/n24q02m/better-telegram-mcp/commit/daef308e8c4157200837e6b48c2662b7f470506b))

- Substitute PUBLIC_URL and derive worker domain in cf-deploy.mjs
  ([#881](https://github.com/n24q02m/better-telegram-mcp/pull/881),
  [`daef308`](https://github.com/n24q02m/better-telegram-mcp/commit/daef308e8c4157200837e6b48c2662b7f470506b))

- Use field-group and semantic labels in credential form
  ([`378b854`](https://github.com/n24q02m/better-telegram-mcp/commit/378b854eb9641842f60e7ae9b0626876c1fbf62e))

- Use placeholders for PUBLIC_URL and routes in wrangler.jsonc (BYO-generic)
  ([#881](https://github.com/n24q02m/better-telegram-mcp/pull/881),
  [`daef308`](https://github.com/n24q02m/better-telegram-mcp/commit/daef308e8c4157200837e6b48c2662b7f470506b))

- **deps**: Update docker/login-action digest to af1e73f
  ([`de36328`](https://github.com/n24q02m/better-telegram-mcp/commit/de3632867c733bcf665ca6d0efcd5244ae24446b))

- **deps**: Update non-major dependencies
  ([#876](https://github.com/n24q02m/better-telegram-mcp/pull/876),
  [`16989be`](https://github.com/n24q02m/better-telegram-mcp/commit/16989beb7538f6ed3ed05cff01f5338a8212173b))

### Chores

- **deps**: Lock file maintenance ([#877](https://github.com/n24q02m/better-telegram-mcp/pull/877),
  [`6b511ff`](https://github.com/n24q02m/better-telegram-mcp/commit/6b511ff7aa39650d4c43776e618beb258fa0d67c))

- **deps**: Update docker/build-push-action digest to 53b7df9
  ([#875](https://github.com/n24q02m/better-telegram-mcp/pull/875),
  [`05cf33c`](https://github.com/n24q02m/better-telegram-mcp/commit/05cf33cb234cb4f978be9da91ff9fc7607ad48ec))

- **deps**: Update docker/setup-buildx-action digest to bb05f3f
  ([#883](https://github.com/n24q02m/better-telegram-mcp/pull/883),
  [`5e172e2`](https://github.com/n24q02m/better-telegram-mcp/commit/5e172e2bc017a83561994806c2efc091f6b8dec5))

### Features

- Add BYO Deploy to Cloudflare section to README
  ([#881](https://github.com/n24q02m/better-telegram-mcp/pull/881),
  [`daef308`](https://github.com/n24q02m/better-telegram-mcp/commit/daef308e8c4157200837e6b48c2662b7f470506b))


## v4.14.0 (2026-07-02)

### Bug Fixes

- Bump mcp-core to 1.18.1 ([#880](https://github.com/n24q02m/better-telegram-mcp/pull/880),
  [`c38334d`](https://github.com/n24q02m/better-telegram-mcp/commit/c38334d08c4636baea3756e14214935dec7a2139))


## v4.14.0-beta.1 (2026-07-02)

### Features

- Deploy CF Worker+Container on release from cd.yml
  ([#878](https://github.com/n24q02m/better-telegram-mcp/pull/878),
  [`e74a7aa`](https://github.com/n24q02m/better-telegram-mcp/commit/e74a7aa8bed00315900334b53fd137c6fffb84d1))


## v4.13.0 (2026-07-01)


## v4.13.0-beta.8 (2026-07-01)

### Bug Fixes

- Align modes-overview link and tool count with current two-transport model
  ([#873](https://github.com/n24q02m/better-telegram-mcp/pull/873),
  [`a24e580`](https://github.com/n24q02m/better-telegram-mcp/commit/a24e580fd30c3042e37ab78b344221d988ea8a09))

### Chores

- **deps**: Lock file maintenance ([#869](https://github.com/n24q02m/better-telegram-mcp/pull/869),
  [`c9cb090`](https://github.com/n24q02m/better-telegram-mcp/commit/c9cb09058277377859b4a9b18baf86d7ec9eb8df))

- **deps**: Update non-major dependencies
  ([#868](https://github.com/n24q02m/better-telegram-mcp/pull/868),
  [`30de287`](https://github.com/n24q02m/better-telegram-mcp/commit/30de287c6867526d6d4355ad04387170949f1c71))

### Features

- **ux**: Add dual-channel validation feedback for credential form
  ([#871](https://github.com/n24q02m/better-telegram-mcp/pull/871),
  [`dd708e8`](https://github.com/n24q02m/better-telegram-mcp/commit/dd708e842446c5e93e18b715e2be36ddc591625f))


## v4.13.0-beta.7 (2026-06-30)

### Bug Fixes

- Canary Gate-A/B settle-retry to avoid false-fail on slow container startup
  ([#862](https://github.com/n24q02m/better-telegram-mcp/pull/862),
  [`f74d480`](https://github.com/n24q02m/better-telegram-mcp/commit/f74d480dfe613a8524489be214b60c7837bd5372))

- Collapse OAuth + per-sub routing to one DO (resolve max_instances=1 deadlock)
  ([#867](https://github.com/n24q02m/better-telegram-mcp/pull/867),
  [`2a15e8d`](https://github.com/n24q02m/better-telegram-mcp/commit/2a15e8d04be5728a685e90e2f71e4fbc6af6037c))

- Lock file maintenance
  ([`9547697`](https://github.com/n24q02m/better-telegram-mcp/commit/9547697a8222b3167441451f7fc2bbd6ca74f616))

- Remove unused function _is_user_mode_config
  ([`c932d44`](https://github.com/n24q02m/better-telegram-mcp/commit/c932d441a6cbfd0f57b34ac503f162688a9b6069))

- Route OAuth /token refresh to the sub's DO to avoid max_instances=1 deadlock
  ([#863](https://github.com/n24q02m/better-telegram-mcp/pull/863),
  [`6924003`](https://github.com/n24q02m/better-telegram-mcp/commit/69240035be366070e0d99629eedde7c8c64402ee))

- Unused function _normalize_for_prefix_check
  ([`8248513`](https://github.com/n24q02m/better-telegram-mcp/commit/8248513c62b3ff583f4574929001504441492539))

### Features

- Add prefers-reduced-motion CSS media query
  ([`acbd99c`](https://github.com/n24q02m/better-telegram-mcp/commit/acbd99c58337d1cb8254380c68480f0adc444af6))


## v4.13.0-beta.6 (2026-06-29)

### Bug Fixes

- Add :active states to credential form + correct session_name log
  ([`a277c5a`](https://github.com/n24q02m/better-telegram-mcp/commit/a277c5aff925592fdfe4c19e8749178e2ff0324a))

- Apply ruff format to satisfy CI format gate
  ([`8f3f4d0`](https://github.com/n24q02m/better-telegram-mcp/commit/8f3f4d0c2ff54fdebc90172371643b02fe97ba83))

- Cap max_instances=1 for CF container cost (solo dev default)
  ([`5398fa0`](https://github.com/n24q02m/better-telegram-mcp/commit/5398fa0cb04af18e8bf83c900c3d7ea9c05430e2))

- Centralize bot-token redaction in error messages
  ([`d6a09fe`](https://github.com/n24q02m/better-telegram-mcp/commit/d6a09fe37836bcf4c0b33d7f18e28c2d2def38c2))

- Cover bot_backend _call error path (token redaction, raise-from-None)
  ([`a979291`](https://github.com/n24q02m/better-telegram-mcp/commit/a979291495cbfb0fea4455f0c13f6b56fe27d597))

- Cover pending_otp_store + KV-restore branch to satisfy 95% coverage gate
  ([`5a78e1a`](https://github.com/n24q02m/better-telegram-mcp/commit/5a78e1a7a4e6f12c1376716e1c9ffb3bdd3e01ad))

- Disconnect telegram sessions concurrently in cleanup and revoke
  ([#830](https://github.com/n24q02m/better-telegram-mcp/pull/830),
  [`12a77c2`](https://github.com/n24q02m/better-telegram-mcp/commit/12a77c2b63f2c8cbb48e774189203e2c759eb9e7))

- Persist OTP state to KV, reduce sleepAfter 1h→5m
  ([`4eee059`](https://github.com/n24q02m/better-telegram-mcp/commit/4eee059fd0ffd9d78ccfadcc83d95ed83d4c6ed2))

- Type _PendingOTP as TypedDict to fix ty not-subscriptable on session_name slice
  ([`7e680fa`](https://github.com/n24q02m/better-telegram-mcp/commit/7e680fa33ea462d181a7017e8b3f343a0a0c1085))

- Update actions/setup-python digest
  ([`6c0f823`](https://github.com/n24q02m/better-telegram-mcp/commit/6c0f8233c6845470531854c65ab7f4f0c7c9daa0))

- Update dawidd6/action-send-mail action
  ([`41ec5b7`](https://github.com/n24q02m/better-telegram-mcp/commit/41ec5b7958bfdced4946282642e376d980096807))

- Update python:3.13-slim-bookworm docker digest
  ([`b816c58`](https://github.com/n24q02m/better-telegram-mcp/commit/b816c5880653ab5570aaee48d35e8797f87cae68))

- Use secrets.token_hex for master-secret generation
  ([`bc4e8db`](https://github.com/n24q02m/better-telegram-mcp/commit/bc4e8dbc0b2c5dd0e9bc473a3402abcaf6f518b2))

- **deps**: Update non-major dependencies
  ([#836](https://github.com/n24q02m/better-telegram-mcp/pull/836),
  [`2ce2dae`](https://github.com/n24q02m/better-telegram-mcp/commit/2ce2dae8fe37d1422d4a3dc4360fa1e03f8d061a))

### Chores

- **deps**: Lock file maintenance ([#820](https://github.com/n24q02m/better-telegram-mcp/pull/820),
  [`a065e91`](https://github.com/n24q02m/better-telegram-mcp/commit/a065e91b903669da31eb07690912870b747f22b9))


## v4.13.0-beta.5 (2026-06-22)

### Bug Fixes

- Bump mcp-core to 1.18.0b19 (relay model-search catalog + OAuth refresh-TTL)
  ([#819](https://github.com/n24q02m/better-telegram-mcp/pull/819),
  [`1b4e2af`](https://github.com/n24q02m/better-telegram-mcp/commit/1b4e2af6353c8e2ce93e6356d450ac6317c16c09))

- Make mcp-core pin guard compare floor version instead of literal string
  ([#819](https://github.com/n24q02m/better-telegram-mcp/pull/819),
  [`1b4e2af`](https://github.com/n24q02m/better-telegram-mcp/commit/1b4e2af6353c8e2ce93e6356d450ac6317c16c09))


## v4.13.0-beta.4 (2026-06-22)

### Bug Fixes

- Pin CF container max_instances to 3
  ([#818](https://github.com/n24q02m/better-telegram-mcp/pull/818),
  [`45815a4`](https://github.com/n24q02m/better-telegram-mcp/commit/45815a457a37b07379a5f4b2e1de07a56a8052c2))

- Repair README doc rot — drop v<auto> placeholder, add Install + Configuration sections
  ([#814](https://github.com/n24q02m/better-telegram-mcp/pull/814),
  [`143b79f`](https://github.com/n24q02m/better-telegram-mcp/commit/143b79fb8b2523ca6a895551aeaa4e378421371a))

### Chores

- **deps**: Lock file maintenance ([#815](https://github.com/n24q02m/better-telegram-mcp/pull/815),
  [`632ef72`](https://github.com/n24q02m/better-telegram-mcp/commit/632ef72b39bc98f564085b8937f4acf751236b43))

### Features

- **ux**: Refine disabled hover states and dynamic labels in auth form
  ([#816](https://github.com/n24q02m/better-telegram-mcp/pull/816),
  [`c872384`](https://github.com/n24q02m/better-telegram-mcp/commit/c872384bdb90e2c13f02562aa3ec42a8a77ca0fc))


## v4.13.0-beta.3 (2026-06-21)

### Bug Fixes

- Add cf:deploy script for live wrangler deploy
  ([#813](https://github.com/n24q02m/better-telegram-mcp/pull/813),
  [`1e1308c`](https://github.com/n24q02m/better-telegram-mcp/commit/1e1308cf759d5c0504cc6656fdc073cc6713a506))

- Make canary gate utf-8-safe (decode+encode) and Cloudflare-UA-aware
  ([`8300810`](https://github.com/n24q02m/better-telegram-mcp/commit/8300810590e7d5a193253a8c3a66f102d8850dae))

- Make canary gate utf-8-safe and Cloudflare-UA-aware
  ([`8300810`](https://github.com/n24q02m/better-telegram-mcp/commit/8300810590e7d5a193253a8c3a66f102d8850dae))

- Neutral default endpoint + env-first secrets in CF self-host scripts
  ([`5662102`](https://github.com/n24q02m/better-telegram-mcp/commit/566210259b3f71d5effa4761ad56e110ecccc23a))

- Right-size CF container to basic instance and cap max_instances at 10
  ([#812](https://github.com/n24q02m/better-telegram-mcp/pull/812),
  [`e11574e`](https://github.com/n24q02m/better-telegram-mcp/commit/e11574eafcd321279ec786639bcead38aebe3474))

- Ruff-format cf_full_flow harness
  ([`49e04d0`](https://github.com/n24q02m/better-telegram-mcp/commit/49e04d014821bc69bfe4e701d5c8bf0fe04c695e))

- Use contextlib.suppress for stdout reconfigure (SIM105)
  ([`8300810`](https://github.com/n24q02m/better-telegram-mcp/commit/8300810590e7d5a193253a8c3a66f102d8850dae))

- **deps**: Update non-major dependencies
  ([#803](https://github.com/n24q02m/better-telegram-mcp/pull/803),
  [`772ca38`](https://github.com/n24q02m/better-telegram-mcp/commit/772ca386fa551571206c1e1aa0022f0e4855756e))

### Chores

- **deps**: Update actions/checkout action to v7
  ([#804](https://github.com/n24q02m/better-telegram-mcp/pull/804),
  [`7d51841`](https://github.com/n24q02m/better-telegram-mcp/commit/7d51841c6e00e265d9f8bd77feed0d5fd6589ed2))

### Features

- Add CF protocol-test harness cf_full_flow.py
  ([`49e04d0`](https://github.com/n24q02m/better-telegram-mcp/commit/49e04d014821bc69bfe4e701d5c8bf0fe04c695e))

- **ux**: Add aria-pressed and color-scheme for a11y and visual polish
  ([#808](https://github.com/n24q02m/better-telegram-mcp/pull/808),
  [`8447aef`](https://github.com/n24q02m/better-telegram-mcp/commit/8447aefe57822c436aba91bbfb93219a9f11825d))


## v4.13.0-beta.2 (2026-06-18)

### Bug Fixes

- Add missing contacts tool tests and strengthen assertions
  ([`a59832a`](https://github.com/n24q02m/better-telegram-mcp/commit/a59832a934997e010ce6df65354c0530f7a0d4a3))

- Bump mcp-core to 1.18.0b10
  ([`5d12678`](https://github.com/n24q02m/better-telegram-mcp/commit/5d12678754d7962a8185cb0b0f28f8958eb362c6))

- Clear validation error state on credential form input
  ([`1eaef66`](https://github.com/n24q02m/better-telegram-mcp/commit/1eaef66bdaebc42f3d8c764ce7b0acf4ebd511d5))

- Correct private-invite link detection in join_chat and add coverage
  ([`57f4ef3`](https://github.com/n24q02m/better-telegram-mcp/commit/57f4ef32d431f0cf7faf6ab36137ab241e268f89))

- Prefix unused account var to satisfy RUF059
  ([`5dd7624`](https://github.com/n24q02m/better-telegram-mcp/commit/5dd7624de35aa37b92acc2e0b82a1ad29c79a0dc))

- Refresh lockfile (renovate maintenance)
  ([`aa00905`](https://github.com/n24q02m/better-telegram-mcp/commit/aa009051d395997cf1675f7bb8c3b87bc9e4dc13))

- Remove stale docstring references to deprecated per_user_session_store.py
  ([`9570e75`](https://github.com/n24q02m/better-telegram-mcp/commit/9570e75d81fef6ffec13a7f08087fd4b8de174b1))

- Revoke expired sessions concurrently in auth cleanup
  ([`c5ac409`](https://github.com/n24q02m/better-telegram-mcp/commit/c5ac409e1f3c13b0aedec12c64365bad77aed35e))

- Update mcp-core pin-guard test to 1.18.0b10 floor
  ([`5d12678`](https://github.com/n24q02m/better-telegram-mcp/commit/5d12678754d7962a8185cb0b0f28f8958eb362c6))

- Update non-major dependencies
  ([`ad441b0`](https://github.com/n24q02m/better-telegram-mcp/commit/ad441b086e936060cdab832d52e5d4099f1061ed))

- Update python base image
  ([`c430245`](https://github.com/n24q02m/better-telegram-mcp/commit/c4302459d62544a063327e6ce28b86b4e280fa93))

- Update typescript to v6
  ([`c185ec4`](https://github.com/n24q02m/better-telegram-mcp/commit/c185ec4bf29fdf90b67c45442cbd4f34f514864f))

- Use shallow copy instead of deepcopy in InMemorySessionStore load paths
  ([`8a4294e`](https://github.com/n24q02m/better-telegram-mcp/commit/8a4294e1a4bef45146f57ef9254ace43c33da7d3))

### Features

- Add CF deploy script with post-deploy canary gate and auto-rollback
  ([`5dd7624`](https://github.com/n24q02m/better-telegram-mcp/commit/5dd7624de35aa37b92acc2e0b82a1ad29c79a0dc))

- Add password visibility toggle to credential form
  ([`8b6a3cf`](https://github.com/n24q02m/better-telegram-mcp/commit/8b6a3cf1ca48fba3d2b6c5fec94bfb4eb39a84f1))


## v4.13.0-beta.1 (2026-06-16)

### Bug Fixes

- Correct stdio credential storage path and dead auth env var in docs
  ([`96d1f0b`](https://github.com/n24q02m/better-telegram-mcp/commit/96d1f0b92473d4edf723a90f09bd64e337b46654))

- Forward MCP_RELAY_PASSWORD into CF container so Gate A is enforced
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Query backend for saved sessions in CF mode (kill FS-glob false-negative)
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Remove dead CredentialStore methods and unused auth_url setting
  ([`6813828`](https://github.com/n24q02m/better-telegram-mcp/commit/681382820112b912ee4a666ab9a3c386e60f782a))

- Remove non-existent auth CLI and config action from AGENTS.md
  ([#759](https://github.com/n24q02m/better-telegram-mcp/pull/759),
  [`f21e720`](https://github.com/n24q02m/better-telegram-mcp/commit/f21e7202e5cd0da1b6ebc408d8438aebf9bb35e0))

- Remove orphaned Qodo pr-agent config
  ([#757](https://github.com/n24q02m/better-telegram-mcp/pull/757),
  [`1285ffb`](https://github.com/n24q02m/better-telegram-mcp/commit/1285ffb9d794909bcdf50505eb86e611d6019662))

- Ruff lint in KvSessionStore (unquoted annotation, unused import)
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Sync README tagline to current capability description
  ([#761](https://github.com/n24q02m/better-telegram-mcp/pull/761),
  [`424f0ca`](https://github.com/n24q02m/better-telegram-mcp/commit/424f0ca54f1347af4e5e807ebe6e4af5aefd57da))

### Features

- Add CF state-survives-recreate + per-sub isolation guards
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Add Cloudflare test harness (fake KV http, Telethon double, env presets)
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Add Cloudflare Worker fronting per-sub Telegram container DO (KV-only)
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Add KvSessionStore for durable per-sub session metadata
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Add wrangler config for KV-only Telegram Worker + container
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Bump mcp-core pin to 1.18.0b7 for storage backend seam
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Bump mcp-core pin to 1.18.0b8 for StringSession seam
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Load per-sub Telethon StringSession from backend with save-on-change
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Migrate to Cloudflare Worker + Container + KV with per-sub multi-user
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Route single-user credentials through backend seam in CF mode
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Select durable KvSessionStore in CF mode for session restore
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))

- Sync cross-promo section ([#762](https://github.com/n24q02m/better-telegram-mcp/pull/762),
  [`631ee54`](https://github.com/n24q02m/better-telegram-mcp/commit/631ee544b981c84646fe5a86f75a7c7cf7baa512))

- Thread storage backend through TelegramAuthProvider into UserBackend
  ([#792](https://github.com/n24q02m/better-telegram-mcp/pull/792),
  [`2467048`](https://github.com/n24q02m/better-telegram-mcp/commit/2467048214ac8a1cd89653aa130326779b2b7d50))


## v4.12.7-beta.3 (2026-06-10)

### Bug Fixes

- Remove deprecated per_user_session_store.py
  ([#751](https://github.com/n24q02m/better-telegram-mcp/pull/751),
  [`adb2b0b`](https://github.com/n24q02m/better-telegram-mcp/commit/adb2b0baf7c792e490c36f799b71b73abced810d))

### Testing

- **media**: Add robust test cases for media tool
  ([#740](https://github.com/n24q02m/better-telegram-mcp/pull/740),
  [`8f22b5c`](https://github.com/n24q02m/better-telegram-mcp/commit/8f22b5cff5f23106b397a2f3fc08488c417e5419))


## v4.12.7-beta.2 (2026-06-10)

### Bug Fixes

- Add Comparison section to README ([#739](https://github.com/n24q02m/better-telegram-mcp/pull/739),
  [`51f3e2c`](https://github.com/n24q02m/better-telegram-mcp/commit/51f3e2c88c3a2d37bf405f6b48cf5f16e10a8224))

- Correct docs drift (versions, tool names, links, compose base)
  ([#738](https://github.com/n24q02m/better-telegram-mcp/pull/738),
  [`b57f423`](https://github.com/n24q02m/better-telegram-mcp/commit/b57f42314371ed63b0e691a133ebfbca09849ed3))


## v4.12.7-beta.1 (2026-06-10)

### Bug Fixes

- SSRF bypass via IPv4-mapped IPv6 and missing blocked ranges
  ([#736](https://github.com/n24q02m/better-telegram-mcp/pull/736),
  [`e379ce3`](https://github.com/n24q02m/better-telegram-mcp/commit/e379ce37e57e132523ec8e1addb02773337eb9a6))

- **deps**: Update non-major dependencies
  ([#734](https://github.com/n24q02m/better-telegram-mcp/pull/734),
  [`1749c1f`](https://github.com/n24q02m/better-telegram-mcp/commit/1749c1f33a0fb92aa0d11275f975e8d044b5029a))

### Chores

- **deps**: Lock file maintenance ([#735](https://github.com/n24q02m/better-telegram-mcp/pull/735),
  [`500c777`](https://github.com/n24q02m/better-telegram-mcp/commit/500c777da22af96c34aeaa720e19bcda60b529d0))

- **deps**: Update step-security/harden-runner digest to 9af89fc
  ([#733](https://github.com/n24q02m/better-telegram-mcp/pull/733),
  [`ff158c2`](https://github.com/n24q02m/better-telegram-mcp/commit/ff158c22a3e893c5cc6b0e79e02d8e311271d77b))


## v4.12.6 (2026-06-09)


## v4.12.6-beta.1 (2026-06-09)

### Bug Fixes

- Gitignore bot/merge junk artifacts (*.orig/*.rej/*.patch/*.diff/*.cover/*.bak)
  ([#711](https://github.com/n24q02m/better-telegram-mcp/pull/711),
  [`1cba315`](https://github.com/n24q02m/better-telegram-mcp/commit/1cba315bebbf2050f4f07ea2fa3e6ac25580af8f))

- **deps**: Update non-major dependencies
  ([#730](https://github.com/n24q02m/better-telegram-mcp/pull/730),
  [`593da59`](https://github.com/n24q02m/better-telegram-mcp/commit/593da59a641985d05857fe5743c168e7891997b1))

### Chores

- **deps**: Update codecov/codecov-action action to v7
  ([#731](https://github.com/n24q02m/better-telegram-mcp/pull/731),
  [`860560c`](https://github.com/n24q02m/better-telegram-mcp/commit/860560c67ee0ed31c0c0e36e66bd2b6d94e95329))


## v4.12.5 (2026-06-07)

### Bug Fixes

- Report package version in serverInfo and honor MCP_PORT in HTTP mode
  ([#709](https://github.com/n24q02m/better-telegram-mcp/pull/709),
  [`51161d8`](https://github.com/n24q02m/better-telegram-mcp/commit/51161d8b4c0b46e3280d705235f0231a49e54cd7))


## v4.12.5-beta.1 (2026-06-07)

### Bug Fixes

- Add whitespace edge-case tests for empty-to-none normalization
  ([`68d54f4`](https://github.com/n24q02m/better-telegram-mcp/commit/68d54f407b49813efdf7ec539a3569387b81d10b))

- Document Glama display-name and ownership configuration in AGENTS.md
  ([`f36882d`](https://github.com/n24q02m/better-telegram-mcp/commit/f36882d85aad6007fa1cfe4cf5395cb4592149f8))

- Remove unused MessagesArgs re-export from tools package
  ([`2d2714b`](https://github.com/n24q02m/better-telegram-mcp/commit/2d2714bb7770076fe78f772dbfd251637272aaba))

- Update actions/checkout digest to df4cb1c
  ([`6550c20`](https://github.com/n24q02m/better-telegram-mcp/commit/6550c20831942584bf353d8fbc6403402aef5cae))

- Update non-major dependencies
  ([`12fda8f`](https://github.com/n24q02m/better-telegram-mcp/commit/12fda8f8be9d07d8b4d7371f36edadaa59f22c7e))

- Use iter_participants async iteration in get_members to reduce memory overhead
  ([`ccbe511`](https://github.com/n24q02m/better-telegram-mcp/commit/ccbe51178b865dc60c61f86326d2ba798481bfcb))

- Wrap IPv6 addresses in brackets when reconstructing URL in fetch_url_safely
  ([`24b960c`](https://github.com/n24q02m/better-telegram-mcp/commit/24b960c36b4b9b3fd72fe01b1efccecbf0dcf118))


## v4.12.4 (2026-06-01)

### Bug Fixes

- Pin mcp-core 1.17.2 (stable)
  ([`82868bc`](https://github.com/n24q02m/better-telegram-mcp/commit/82868bc2a1e67eae599987683db842b04bf8d916))


## v4.12.4-beta.1 (2026-06-01)

### Bug Fixes

- Accept cross-stack MCP_DCR_SERVER_SECRET (legacy DCR_SERVER_SECRET still works)
  ([#627](https://github.com/n24q02m/better-telegram-mcp/pull/627),
  [`48ff4a4`](https://github.com/n24q02m/better-telegram-mcp/commit/48ff4a4cef06c39a4e02b0592fa7e869af7f1853))

- Apply ruff format to new http transport tests
  ([#627](https://github.com/n24q02m/better-telegram-mcp/pull/627),
  [`48ff4a4`](https://github.com/n24q02m/better-telegram-mcp/commit/48ff4a4cef06c39a4e02b0592fa7e869af7f1853))

- Bump mcp-core to 1.17.2-beta.1 for beta testing
  ([`c6bd7b2`](https://github.com/n24q02m/better-telegram-mcp/commit/c6bd7b20b3065807f0e194cb31cab24494f10b72))

- Strip whitespace before URL scheme check to close SSRF bypass
  ([#620](https://github.com/n24q02m/better-telegram-mcp/pull/620),
  [`b4c2457`](https://github.com/n24q02m/better-telegram-mcp/commit/b4c2457403a2ca8aa5111f399c625003775f98e9))

- Sync docs to code (DCR_SERVER_SECRET env name, drop dead setup-manual link)
  ([#626](https://github.com/n24q02m/better-telegram-mcp/pull/626),
  [`fcb186f`](https://github.com/n24q02m/better-telegram-mcp/commit/fcb186fcfe989f0c28c233c2784d0ef5fae5508b))

- Update non-major dependencies (mcp, starlette)
  ([#612](https://github.com/n24q02m/better-telegram-mcp/pull/612),
  [`7899030`](https://github.com/n24q02m/better-telegram-mcp/commit/7899030a9a5ab2a9280dad973e419fef93405e32))

- Uv lock file maintenance ([#613](https://github.com/n24q02m/better-telegram-mcp/pull/613),
  [`89ef4f9`](https://github.com/n24q02m/better-telegram-mcp/commit/89ef4f99c68c48cb106ff5a8a4dfbe455b3052dc))


## v4.12.3 (2026-05-29)

### Bug Fixes

- Pin mcp-core 1.17.1 (BearerMCPApp resource_metadata #260)
  ([`e87d0f5`](https://github.com/n24q02m/better-telegram-mcp/commit/e87d0f53a5241b0e27dcdca822242f55b3f0f43b))


## v4.12.2 (2026-05-29)

### Bug Fixes

- Canonicalize blocked-path check to close firmlink bypass
  ([#606](https://github.com/n24q02m/better-telegram-mcp/pull/606),
  [`ce26113`](https://github.com/n24q02m/better-telegram-mcp/commit/ce261133a33878b55628b77d221288f446a0e5aa))

- Pin mcp-core 1.17.0 (stable OAuth refresh_token)
  ([`1cb7ebf`](https://github.com/n24q02m/better-telegram-mcp/commit/1cb7ebfd298853860e70f09e4924ad939c591f11))

- Redact Telegram bot token from error messages
  ([#605](https://github.com/n24q02m/better-telegram-mcp/pull/605),
  [`7d020d7`](https://github.com/n24q02m/better-telegram-mcp/commit/7d020d7ea2cf461b949816a77af2e4f2e43ec190))


## v4.12.2-beta.1 (2026-05-29)

### Bug Fixes

- Add backend exception test for server.message
  ([#584](https://github.com/n24q02m/better-telegram-mcp/pull/584),
  [`2256c2c`](https://github.com/n24q02m/better-telegram-mcp/commit/2256c2c52e031348569c7503ec696a8c9c72ada8))

- Add edge case tests for _sanitize_error
  ([#570](https://github.com/n24q02m/better-telegram-mcp/pull/570),
  [`2d2de96`](https://github.com/n24q02m/better-telegram-mcp/commit/2d2de964d4812dd32200b466228e6b0008209f55))

- Add edge case tests for format safe_error
  ([#590](https://github.com/n24q02m/better-telegram-mcp/pull/590),
  [`e9860ee`](https://github.com/n24q02m/better-telegram-mcp/commit/e9860eeb245592520d8b68daafc3a8880a8acfbd))

- Add tests for _not_ready_response
  ([#567](https://github.com/n24q02m/better-telegram-mcp/pull/567),
  [`03bb146`](https://github.com/n24q02m/better-telegram-mcp/commit/03bb146fe92c5244e5caec07c6327649b5dc806a))

- Add tests for config helpers ([#573](https://github.com/n24q02m/better-telegram-mcp/pull/573),
  [`fae196b`](https://github.com/n24q02m/better-telegram-mcp/commit/fae196b2c4e1ec0d22712977054c52b5f28777af))

- Bump mcp-core to 1.17.0-beta.1 for OAuth refresh_token
  ([`8213a6e`](https://github.com/n24q02m/better-telegram-mcp/commit/8213a6e9703175a75c8e9f60875670ac016455d8))

- Lock file maintenance ([#604](https://github.com/n24q02m/better-telegram-mcp/pull/604),
  [`ea94742`](https://github.com/n24q02m/better-telegram-mcp/commit/ea94742e02a4753051bcbd3d0dedf7b38207f8a9))

- Parametrize 2fa password detection tests
  ([#576](https://github.com/n24q02m/better-telegram-mcp/pull/576),
  [`5e2097c`](https://github.com/n24q02m/better-telegram-mcp/commit/5e2097c2c1717d232f37486b594b2bf0db9f3e90))

- Prevent SSRF via DNS rebinding by pinning resolved IP on media fetch
  ([#600](https://github.com/n24q02m/better-telegram-mcp/pull/600),
  [`e4fae7a`](https://github.com/n24q02m/better-telegram-mcp/commit/e4fae7afea7878de950c24428a6e7b6dbeb3d525))

- Remove unused __future__ annotations import in __main__
  ([#568](https://github.com/n24q02m/better-telegram-mcp/pull/568),
  [`f4cc003`](https://github.com/n24q02m/better-telegram-mcp/commit/f4cc00396f0ac6157acd2b1554690cf759252de2))

- Remove unused __future__ annotations import in auth/in_memory_session_store
  ([#572](https://github.com/n24q02m/better-telegram-mcp/pull/572),
  [`20e7860`](https://github.com/n24q02m/better-telegram-mcp/commit/20e786082a91ea42c9706644f7acfdb73833811f))

- Remove unused __future__ annotations import in credential_form
  ([#574](https://github.com/n24q02m/better-telegram-mcp/pull/574),
  [`66c0053`](https://github.com/n24q02m/better-telegram-mcp/commit/66c005336ceff710f2758f79ad66b8e70f8ea2a7))

- Remove unused __future__ annotations import in credential_state
  ([#580](https://github.com/n24q02m/better-telegram-mcp/pull/580),
  [`cd84e1a`](https://github.com/n24q02m/better-telegram-mcp/commit/cd84e1aea72c49a87e7819c4ea735fee52394a1f))

- Remove unused __future__ annotations import in tools/chats
  ([#591](https://github.com/n24q02m/better-telegram-mcp/pull/591),
  [`02f9601`](https://github.com/n24q02m/better-telegram-mcp/commit/02f960141d513c980a668214bdb9e270d37a8fe2))

- Remove unused __future__ annotations import in tools/config_tool
  ([#577](https://github.com/n24q02m/better-telegram-mcp/pull/577),
  [`ede4930`](https://github.com/n24q02m/better-telegram-mcp/commit/ede4930fc2d47d73748bbddbfd47e5ea27415cb5))

- Remove unused __future__ annotations import in transports/credential_store
  ([#563](https://github.com/n24q02m/better-telegram-mcp/pull/563),
  [`0e952c5`](https://github.com/n24q02m/better-telegram-mcp/commit/0e952c51d9e1defb7cc14cf0f6b6f2c34b2fc2eb))

- Remove unused __future__ annotations import in transports/http
  ([#581](https://github.com/n24q02m/better-telegram-mcp/pull/581),
  [`7129ea2`](https://github.com/n24q02m/better-telegram-mcp/commit/7129ea2aa43c897f0309056f0c1795f377b7cafa))

- Remove unused annotations import in contacts
  ([#571](https://github.com/n24q02m/better-telegram-mcp/pull/571),
  [`ba2b05f`](https://github.com/n24q02m/better-telegram-mcp/commit/ba2b05fad9d94e6da3420d13bb338b6f937fdb6e))

- Remove unused annotations import in formatting
  ([#578](https://github.com/n24q02m/better-telegram-mcp/pull/578),
  [`01f4b62`](https://github.com/n24q02m/better-telegram-mcp/commit/01f4b6246a7a87d8eabb4a0297e9db6c216bf005))

- Remove unused annotations import in messages
  ([#575](https://github.com/n24q02m/better-telegram-mcp/pull/575),
  [`514cddc`](https://github.com/n24q02m/better-telegram-mcp/commit/514cddc34b6d8f09e4a212c453f553819439c675))

- Remove unused annotations import in resources
  ([#564](https://github.com/n24q02m/better-telegram-mcp/pull/564),
  [`fb87ad5`](https://github.com/n24q02m/better-telegram-mcp/commit/fb87ad588e8b42bf3c378dbb7ec1a3c3962e0f40))

- Update non-major dependencies ([#603](https://github.com/n24q02m/better-telegram-mcp/pull/603),
  [`4c6db2a`](https://github.com/n24q02m/better-telegram-mcp/commit/4c6db2a08c2264f40af29c96e372b5b5c93fbffc))

- Use random per-install salt for PBKDF2 key derivation
  ([#593](https://github.com/n24q02m/better-telegram-mcp/pull/593),
  [`87dd227`](https://github.com/n24q02m/better-telegram-mcp/commit/87dd2276cd7b45fbb358a59a671ec70d746ec9a9))


## v4.12.1 (2026-05-28)

### Bug Fixes

- Drop local path source for mcp-core to align with PyPI-only pattern
  ([`c7209fd`](https://github.com/n24q02m/better-telegram-mcp/commit/c7209fdf7612c602c0bb1c41f5cb37ed0a240bb4))


## v4.12.1-beta.1 (2026-05-28)

### Bug Fixes

- **deps**: Pin pydantic to <2.13 to match mcp-core 1.15.0 transitive cap
  ([`36c01e0`](https://github.com/n24q02m/better-telegram-mcp/commit/36c01e0f3dc0afb81ce0342ef85cb17b45168b23))

- **deps**: Update non-major dependencies
  ([#558](https://github.com/n24q02m/better-telegram-mcp/pull/558),
  [`2ff9084`](https://github.com/n24q02m/better-telegram-mcp/commit/2ff9084f0175066c1cffd90fd066dd20b29946ee))

### Performance Improvements

- **backend**: Revert get_messages to iter_messages to save memory
  ([#560](https://github.com/n24q02m/better-telegram-mcp/pull/560),
  [`77a220e`](https://github.com/n24q02m/better-telegram-mcp/commit/77a220e22acf298dc9162a7f64c8560a256a6659))


## v4.12.0 (2026-05-26)


## v4.12.0-beta.4 (2026-05-26)

### Features

- Wire MCP_AUTH_DISABLE env to run_http_server(auth_disabled=)
  ([`983320f`](https://github.com/n24q02m/better-telegram-mcp/commit/983320f0f8d692a38321dcce212f8da1e5863115))


## v4.12.0-beta.3 (2026-05-26)

### Features

- Add MCP_AUTH_DISABLE env flag for external auth boundary
  ([`19ea02f`](https://github.com/n24q02m/better-telegram-mcp/commit/19ea02fdc5d935ff7854bdcae4a5874d7a31dd40))

- **ux**: Improve credential form accessibility
  ([#553](https://github.com/n24q02m/better-telegram-mcp/pull/553),
  [`aa94c0f`](https://github.com/n24q02m/better-telegram-mcp/commit/aa94c0f5f923e336520b2a906c48b918cbdff77e))

- **ux**: Restore focus on network error in credential form
  ([#552](https://github.com/n24q02m/better-telegram-mcp/pull/552),
  [`274f785`](https://github.com/n24q02m/better-telegram-mcp/commit/274f78546deb625adce551698b79e4619ad57ba1))


## v4.12.0-beta.2 (2026-05-24)

### Bug Fixes

- **deps**: Regenerate uv.lock with UV_NO_SOURCES for Docker compatibility
  ([`b5d0ec4`](https://github.com/n24q02m/better-telegram-mcp/commit/b5d0ec4847aced86e47f71b148c70edbff013946))


## v4.12.0-beta.1 (2026-05-24)

### Bug Fixes

- Close TOCTOU window in atomic file writes, parallelize shutdown
  ([#543](https://github.com/n24q02m/better-telegram-mcp/pull/543),
  [`c33653f`](https://github.com/n24q02m/better-telegram-mcp/commit/c33653ff39dcf082dc93cb7539fad833c7ceeee5))

- **ci**: Open files in binary mode on Windows in atomic write helper
  ([#543](https://github.com/n24q02m/better-telegram-mcp/pull/543),
  [`c33653f`](https://github.com/n24q02m/better-telegram-mcp/commit/c33653ff39dcf082dc93cb7539fad833c7ceeee5))

- **ci**: Skip POSIX mode-bit assertions on Windows
  ([#543](https://github.com/n24q02m/better-telegram-mcp/pull/543),
  [`c33653f`](https://github.com/n24q02m/better-telegram-mcp/commit/c33653ff39dcf082dc93cb7539fad833c7ceeee5))

- **deps**: Bump idna to 3.16 + python-multipart to 0.0.29 (Dependabot security alerts)
  ([`9279f38`](https://github.com/n24q02m/better-telegram-mcp/commit/9279f38c27349a13ddc7fa5fc5f57e4ecdbf3456))

- **deps**: Pin pydantic <2.13 for mcp-core 1.14.0 compatibility
  ([#509](https://github.com/n24q02m/better-telegram-mcp/pull/509),
  [`88f3364`](https://github.com/n24q02m/better-telegram-mcp/commit/88f3364acdb3bcd2261456b80a8753d18d1db286))

- **deps**: Update non-major dependencies
  ([#509](https://github.com/n24q02m/better-telegram-mcp/pull/509),
  [`88f3364`](https://github.com/n24q02m/better-telegram-mcp/commit/88f3364acdb3bcd2261456b80a8753d18d1db286))

- **form**: Semantic autocomplete hints for mobile autofill + password managers
  ([#543](https://github.com/n24q02m/better-telegram-mcp/pull/543),
  [`c33653f`](https://github.com/n24q02m/better-telegram-mcp/commit/c33653ff39dcf082dc93cb7539fad833c7ceeee5))

- **security**: Atomic 0o600 file creation to close TOCTOU race
  ([#543](https://github.com/n24q02m/better-telegram-mcp/pull/543),
  [`c33653f`](https://github.com/n24q02m/better-telegram-mcp/commit/c33653ff39dcf082dc93cb7539fad833c7ceeee5))

### Chores

- **deps**: Update actions/create-github-app-token digest to bcd2ba4
  ([#519](https://github.com/n24q02m/better-telegram-mcp/pull/519),
  [`c365848`](https://github.com/n24q02m/better-telegram-mcp/commit/c365848a2c122d488ee27516db9045f11701e9b2))

- **deps**: Update actions/dependency-review-action action to v5
  ([#510](https://github.com/n24q02m/better-telegram-mcp/pull/510),
  [`afcca41`](https://github.com/n24q02m/better-telegram-mcp/commit/afcca41f0b2a71e6373ef2e958ea3981fc4548e3))

- **deps**: Update codecov/codecov-action digest to e79a696
  ([#544](https://github.com/n24q02m/better-telegram-mcp/pull/544),
  [`fb9a751`](https://github.com/n24q02m/better-telegram-mcp/commit/fb9a75145a452e18a0f32a8b115831261968c948))

- **deps**: Update docker/build-push-action digest to f9f3042
  ([#545](https://github.com/n24q02m/better-telegram-mcp/pull/545),
  [`d0b6c9f`](https://github.com/n24q02m/better-telegram-mcp/commit/d0b6c9fc7c9d1a5d587682bab440a60419cd8509))

- **deps**: Update docker/login-action digest to 650006c
  ([#546](https://github.com/n24q02m/better-telegram-mcp/pull/546),
  [`dc8e1fb`](https://github.com/n24q02m/better-telegram-mcp/commit/dc8e1fbc8cbd6bc974549ee5a5f8c192b7746db6))

- **deps**: Update docker/setup-buildx-action digest to d7f5e7f
  ([#547](https://github.com/n24q02m/better-telegram-mcp/pull/547),
  [`905c496`](https://github.com/n24q02m/better-telegram-mcp/commit/905c496b7f6ef90b12ba1d72c1bc686e3f22e2fc))

- **deps**: Update python:3.13-slim-bookworm docker digest to e4fa1f9
  ([#512](https://github.com/n24q02m/better-telegram-mcp/pull/512),
  [`6447163`](https://github.com/n24q02m/better-telegram-mcp/commit/64471634c7ef73110b9b3d007bb37163a75d3ecd))

- **deps**: Update step-security/harden-runner digest to ab7a940
  ([#523](https://github.com/n24q02m/better-telegram-mcp/pull/523),
  [`32cd58b`](https://github.com/n24q02m/better-telegram-mcp/commit/32cd58bec9f1ff9c92390e9e648d548fc88f6f72))

### Features

- **a11y**: Add aria-live and roles to dynamic status messages
  ([#550](https://github.com/n24q02m/better-telegram-mcp/pull/550),
  [`2d46d37`](https://github.com/n24q02m/better-telegram-mcp/commit/2d46d3769a1046ec606d8ac77d1f0018e3e32089))

### Performance Improvements

- **shutdown**: Disconnect Telegram backends concurrently via asyncio.gather
  ([#543](https://github.com/n24q02m/better-telegram-mcp/pull/543),
  [`c33653f`](https://github.com/n24q02m/better-telegram-mcp/commit/c33653ff39dcf082dc93cb7539fad833c7ceeee5))


## v4.11.0 (2026-05-09)


## v4.11.0-beta.2 (2026-05-08)

### Bug Fixes

- **deps**: Regenerate uv.lock without path sources for Docker compatibility
  ([`05962da`](https://github.com/n24q02m/better-telegram-mcp/commit/05962da0f26eb84f5c96f397adc5a38d3c58a583))


## v4.11.0-beta.1 (2026-05-08)

### Bug Fixes

- Add disabled states and form locking during credential submission
  ([`ed9e8f0`](https://github.com/n24q02m/better-telegram-mcp/commit/ed9e8f0d07f6c498a9c0a8e2a369de6d6a6ad11b))

- Add server.json title for Glama display name
  ([`573a0a6`](https://github.com/n24q02m/better-telegram-mcp/commit/573a0a6919ba419d3906a2adaf2ee244143abb58))

- Extract helpers from _lifespan
  ([`4ab81bc`](https://github.com/n24q02m/better-telegram-mcp/commit/4ab81bc5f3b985c221c096a8dc0aa71ba817d30b))

- Extract helpers from start_user_auth
  ([`8860214`](https://github.com/n24q02m/better-telegram-mcp/commit/8860214afc64b4d8c5e19d7ba8cf9e5337dd870c))

- Replace iter_dialogs with get_dialogs in list_chats
  ([`f3b8aeb`](https://github.com/n24q02m/better-telegram-mcp/commit/f3b8aeb07270876b9fd988db73d4508c98b42179))

- Replace iter_messages with get_messages in get_history
  ([`784867d`](https://github.com/n24q02m/better-telegram-mcp/commit/784867da199d25d36d4c12a4c3ee45dadd8f0971))

- Replace iter_participants with get_participants in get_members
  ([`75d36f5`](https://github.com/n24q02m/better-telegram-mcp/commit/75d36f56c74a3598f70b837d0bd35c9ef2483366))

- Switch tuple membership tests to sets across 4 files
  ([`6d237b2`](https://github.com/n24q02m/better-telegram-mcp/commit/6d237b2e2943f341347abf00c324ab5d76561ead))

- Update setup-manual.md refs in error messages to mcp.n24q02m.com
  ([`dea58f9`](https://github.com/n24q02m/better-telegram-mcp/commit/dea58f991cc312a0e2683d9b8cee84bcd6c6e8c1))

- Use set for help topic membership test
  ([`cd4e100`](https://github.com/n24q02m/better-telegram-mcp/commit/cd4e100b8669badcbb70f323dce6d3bfc00e33bd))

- **deps**: Bump n24q02m-mcp-core to 1.14.0
  ([`f816f1e`](https://github.com/n24q02m/better-telegram-mcp/commit/f816f1ebb324e8bccc7281d59f59136bf968b35f))

### Features

- Add bot-mode required-attr tests for credential form
  ([`4ce1bcc`](https://github.com/n24q02m/better-telegram-mcp/commit/4ce1bcc8fa9d8d4233b37853496486474dc392f6))

- Add edge-case tests for formatting utilities
  ([`b2f00db`](https://github.com/n24q02m/better-telegram-mcp/commit/b2f00db16aa0a5297932ab70d019051d9c661be7))

- Add help_tool cache-hit test
  ([`7ac1c2a`](https://github.com/n24q02m/better-telegram-mcp/commit/7ac1c2a62ec58617f79bf321ffaff747b14fc64d))

- Add set_setup_url helper and tests for credential_state
  ([`242edbc`](https://github.com/n24q02m/better-telegram-mcp/commit/242edbcd88345a2079fd610a40c293b078fff615))

- Add Table of contents heading + auto-generated link list (Spec E Wave 2)
  ([`469ba3b`](https://github.com/n24q02m/better-telegram-mcp/commit/469ba3b107fbdf199375c41fed09813a62678d9a))

- Add tests for create_http_mcp_server and run_http
  ([`93ce5fa`](https://github.com/n24q02m/better-telegram-mcp/commit/93ce5fad115f0ea8dd01aa7b2a7f137becaeb2ba))

- Add typo-suggestion and SecurityError tests for contacts
  ([`bf16bda`](https://github.com/n24q02m/better-telegram-mcp/commit/bf16bda8d62df8a2f251115c5713e1a40f28c2e3))

- Add typo-suggestion and settings tests for chats
  ([`6a6a64c`](https://github.com/n24q02m/better-telegram-mcp/commit/6a6a64c8821540f095f44393d03b756a49c4eb01))

- Add typo-suggestion tests for messages tool
  ([`180d572`](https://github.com/n24q02m/better-telegram-mcp/commit/180d572e7a19ad5846c7347176e7cd19762755b6))

- Add unit tests for resource registration
  ([`68483c4`](https://github.com/n24q02m/better-telegram-mcp/commit/68483c49e32206d8929ddd8f220b7635562d87ee))

- Cover SSRF mixed-IP and macOS firmlink paths
  ([`5ce37ae`](https://github.com/n24q02m/better-telegram-mcp/commit/5ce37ae59f5b93a7aeda69431bc68277f24afd52))

- Link to mcp.n24q02m.com unified docs site (Spec F Phase 4)
  ([`a725a00`](https://github.com/n24q02m/better-telegram-mcp/commit/a725a000c2c354a2b81bd722b7c4942fe423a8a7))

- Organize transport tests under test_transports
  ([`fc67847`](https://github.com/n24q02m/better-telegram-mcp/commit/fc678477c0f71567df5e02fc803ef8b42296e956))

- Sync cross-promo section ([#505](https://github.com/n24q02m/better-telegram-mcp/pull/505),
  [`415b319`](https://github.com/n24q02m/better-telegram-mcp/commit/415b319c70d9194e965b68b8ac43232388c6815c))

- Tighten media tool error-message assertions
  ([`8f7dc1e`](https://github.com/n24q02m/better-telegram-mcp/commit/8f7dc1ee5f507031476ce743a54db8286029c81e))

### Testing

- Improve coverage for credential_state.py
  ([`242edbc`](https://github.com/n24q02m/better-telegram-mcp/commit/242edbcd88345a2079fd610a40c293b078fff615))

- Improve coverage for credential_state.py and fix lint
  ([`242edbc`](https://github.com/n24q02m/better-telegram-mcp/commit/242edbcd88345a2079fd610a40c293b078fff615))


## v4.10.0 (2026-05-06)


## v4.10.0-beta.1 (2026-05-06)

### Bug Fixes

- Consolidate setup docs body to 3 methods (drop legacy Method 4/5)
  ([#455](https://github.com/n24q02m/better-telegram-mcp/pull/455),
  [`6c26daf`](https://github.com/n24q02m/better-telegram-mcp/commit/6c26dafbaf6778ceadc7d727a6d70e2377f52270))

- Remove TELEGRAM_PHONE from userConfig (stdio = bot mode only per spec V9)
  ([#460](https://github.com/n24q02m/better-telegram-mcp/pull/460),
  [`a9168e8`](https://github.com/n24q02m/better-telegram-mcp/commit/a9168e8fc4f5a9e2ebd393f89ef8caf3cc32c7ec))

- Revert pydantic to <2.13 to match mcp-core cap
  ([`f7a7485`](https://github.com/n24q02m/better-telegram-mcp/commit/f7a74857bf3becaaa9a5e56c59dd0d287731e971))

- Sync uv.lock version after v4.9.0 release commit
  ([`17ac5f2`](https://github.com/n24q02m/better-telegram-mcp/commit/17ac5f2659d93303538f3997791e1956f694c289))

- **deps**: Update dependency cryptography to v48
  ([#464](https://github.com/n24q02m/better-telegram-mcp/pull/464),
  [`d9b9c99`](https://github.com/n24q02m/better-telegram-mcp/commit/d9b9c99405181b2987fdb843adddb2423e744bee))

- **deps**: Update non-major dependencies
  ([#437](https://github.com/n24q02m/better-telegram-mcp/pull/437),
  [`82c925a`](https://github.com/n24q02m/better-telegram-mcp/commit/82c925a2e56e092e169f4d3b96b0156d1d51e959))

### Chores

- **deps**: Update step-security/harden-runner digest to a5ad31d
  ([#436](https://github.com/n24q02m/better-telegram-mcp/pull/436),
  [`1fe3621`](https://github.com/n24q02m/better-telegram-mcp/commit/1fe362153f810870095e7fe3c37def31d4a5e1f9))

### Features

- Add explicit Method overview section to setup docs
  ([#454](https://github.com/n24q02m/better-telegram-mcp/pull/454),
  [`dd31227`](https://github.com/n24q02m/better-telegram-mcp/commit/dd312275dce2b2ff7385974d520f34ba338ef6fe))

- Align userConfig with relay_schema fields
  ([#459](https://github.com/n24q02m/better-telegram-mcp/pull/459),
  [`544f0af`](https://github.com/n24q02m/better-telegram-mcp/commit/544f0af63fe2bdc65545ad68acaec7dd9ad5f009))

- Clarify Method 1/2/3 mutually exclusive (CC scope-by-endpoint)
  ([#463](https://github.com/n24q02m/better-telegram-mcp/pull/463),
  [`4af35f3`](https://github.com/n24q02m/better-telegram-mcp/commit/4af35f34178547dabfa99c01ccd1be1f6c2dac36))

- Declare userConfig schema and document install prompt
  ([#456](https://github.com/n24q02m/better-telegram-mcp/pull/456),
  [`a92cab1`](https://github.com/n24q02m/better-telegram-mcp/commit/a92cab153f2e048c9d11b775d7d607b0128d8a6f))

- Document userConfig credential prompts per plugin
  ([#461](https://github.com/n24q02m/better-telegram-mcp/pull/461),
  [`ce8d10e`](https://github.com/n24q02m/better-telegram-mcp/commit/ce8d10e8866db1fc52efc1999a93f85358d7d133))


## v4.9.0 (2026-05-04)

### Bug Fixes

- Bump mcp-core to 1.13.0 (STABLE) ([#453](https://github.com/n24q02m/better-telegram-mcp/pull/453),
  [`de541ca`](https://github.com/n24q02m/better-telegram-mcp/commit/de541cae72a67f72de3a1f0de89553b6f3b5ea5e))


## v4.9.0-beta.14 (2026-05-04)

### Bug Fixes

- Re-lock uv.lock without path source so Docker --frozen succeeds
  ([#451](https://github.com/n24q02m/better-telegram-mcp/pull/451),
  [`f8ef48e`](https://github.com/n24q02m/better-telegram-mcp/commit/f8ef48ee186907baad2e7dade6128a70190d06ea))

- Wire create_http_mcp_server() + auth_scope diagnostic log
  ([#451](https://github.com/n24q02m/better-telegram-mcp/pull/451),
  [`f8ef48e`](https://github.com/n24q02m/better-telegram-mcp/commit/f8ef48ee186907baad2e7dade6128a70190d06ea))

- Wire create_http_mcp_server() + diagnostic log + test fixture reset _multi_user_mode
  ([#451](https://github.com/n24q02m/better-telegram-mcp/pull/451),
  [`f8ef48e`](https://github.com/n24q02m/better-telegram-mcp/commit/f8ef48ee186907baad2e7dade6128a70190d06ea))


## v4.9.0-beta.13 (2026-05-04)

### Bug Fixes

- Re-lock uv.lock without path source so Docker --frozen succeeds
  ([#450](https://github.com/n24q02m/better-telegram-mcp/pull/450),
  [`79961c5`](https://github.com/n24q02m/better-telegram-mcp/commit/79961c5117af9028dc541aef8e2886c8bba6b713))


## v4.9.0-beta.12 (2026-05-04)

### Bug Fixes

- Re-lock uv.lock without path source so Docker --frozen succeeds
  ([#449](https://github.com/n24q02m/better-telegram-mcp/pull/449),
  [`53630c1`](https://github.com/n24q02m/better-telegram-mcp/commit/53630c16f0598eb6261185a180b9afbc5caeeb9c))


## v4.9.0-beta.11 (2026-05-04)

### Bug Fixes

- Re-lock uv.lock without path source so Docker --frozen succeeds
  ([#448](https://github.com/n24q02m/better-telegram-mcp/pull/448),
  [`8c0ed64`](https://github.com/n24q02m/better-telegram-mcp/commit/8c0ed644521d0c8e4f4b1cefeb7c865df9861924))


## v4.9.0-beta.10 (2026-05-04)

### Bug Fixes

- Cover multi-user save_credentials and on_step_submitted branches
  ([#447](https://github.com/n24q02m/better-telegram-mcp/pull/447),
  [`765e203`](https://github.com/n24q02m/better-telegram-mcp/commit/765e203b699d5dcf17f029d388a8cc834c806f43))

- Refactor multi-user HTTP to mcp-core run_http_server (drop relay-core)
  ([#447](https://github.com/n24q02m/better-telegram-mcp/pull/447),
  [`765e203`](https://github.com/n24q02m/better-telegram-mcp/commit/765e203b699d5dcf17f029d388a8cc834c806f43))


## v4.9.0-beta.9 (2026-05-03)

### Bug Fixes

- Bump mcp-core to 1.13.0-beta.9 for /login form shell refactor
  ([#444](https://github.com/n24q02m/better-telegram-mcp/pull/444),
  [`2e47dbb`](https://github.com/n24q02m/better-telegram-mcp/commit/2e47dbbc5b66b946d65b9240f30fd9bc067993e9))


## v4.9.0-beta.8 (2026-05-03)

### Features

- Wire /login relay-password gate into multi-user oauth_server
  ([#443](https://github.com/n24q02m/better-telegram-mcp/pull/443),
  [`0ee389a`](https://github.com/n24q02m/better-telegram-mcp/commit/0ee389a0684592a7b43e115d7ac663357afd8104))


## v4.9.0-beta.7 (2026-05-03)

### Features

- Bump mcp-core to 1.13.0-beta.7 ([#442](https://github.com/n24q02m/better-telegram-mcp/pull/442),
  [`7b71df5`](https://github.com/n24q02m/better-telegram-mcp/commit/7b71df53789481aa22dfa166512568e7951a8dfa))

- Document MCP_RELAY_PASSWORD edge auth gate
  ([#441](https://github.com/n24q02m/better-telegram-mcp/pull/441),
  [`0e0c8ba`](https://github.com/n24q02m/better-telegram-mcp/commit/0e0c8ba706979fd7971b2eb917afe32b239efcd9))

- Pass MCP_RELAY_PASSWORD env to HTTP container
  ([#440](https://github.com/n24q02m/better-telegram-mcp/pull/440),
  [`06024d8`](https://github.com/n24q02m/better-telegram-mcp/commit/06024d8b5d0ee550ab7d1b60c0fb3dcb2a368921))


## v4.9.0-beta.6 (2026-05-02)

### Bug Fixes

- Regenerate uv.lock UV_NO_SOURCES=1 (Docker build trap)
  ([#435](https://github.com/n24q02m/better-telegram-mcp/pull/435),
  [`eb90157`](https://github.com/n24q02m/better-telegram-mcp/commit/eb90157cd6a2c35631b51a8a9f45d0c319bcb634))


## v4.9.0-beta.5 (2026-05-02)

### Bug Fixes

- Setup docs + README reflect stdio-pure architecture
  ([#434](https://github.com/n24q02m/better-telegram-mcp/pull/434),
  [`1fe4d2a`](https://github.com/n24q02m/better-telegram-mcp/commit/1fe4d2acccc6693f8078f7b2ce647416169600f2))

### Chores

- **deps**: Update dawidd6/action-send-mail action to v17
  ([#422](https://github.com/n24q02m/better-telegram-mcp/pull/422),
  [`6e214b9`](https://github.com/n24q02m/better-telegram-mcp/commit/6e214b9d0475fde4a36f463b13532d91699dc02f))

### Features

- Stdio-pure + http-multi-user (drop daemon-bridge)
  ([#433](https://github.com/n24q02m/better-telegram-mcp/pull/433),
  [`1e6588b`](https://github.com/n24q02m/better-telegram-mcp/commit/1e6588b60d6e182d7e58120667631d63537b68e6))


## v4.9.0-beta.4 (2026-04-30)

### Bug Fixes

- Regenerate uv.lock with UV_NO_SOURCES=1 to remove local path references
  ([#428](https://github.com/n24q02m/better-telegram-mcp/pull/428),
  [`bccf15b`](https://github.com/n24q02m/better-telegram-mcp/commit/bccf15bf1c5962811e2bd95d18c8ebcadf3f3433))

### Features

- **auth**: Migrate to in-memory session store (TC-NearZK)
  ([#429](https://github.com/n24q02m/better-telegram-mcp/pull/429),
  [`7cf5304`](https://github.com/n24q02m/better-telegram-mcp/commit/7cf5304255615b5b3b820e2c8b79221656178b2c))

- **docs**: Add trust model section to README
  ([#428](https://github.com/n24q02m/better-telegram-mcp/pull/428),
  [`bccf15b`](https://github.com/n24q02m/better-telegram-mcp/commit/bccf15bf1c5962811e2bd95d18c8ebcadf3f3433))


## v4.9.0-beta.3 (2026-04-30)

### Bug Fixes

- Regenerate uv.lock with UV_NO_SOURCES=1 to remove local path references
  ([#426](https://github.com/n24q02m/better-telegram-mcp/pull/426),
  [`f950492`](https://github.com/n24q02m/better-telegram-mcp/commit/f9504921a29eddaa7fd056dc1acd8f57f55dacc0))


## v4.9.0-beta.2 (2026-04-30)

### Bug Fixes

- Strip [tool.uv.sources] in Dockerfile to fix uv sync --frozen Docker build
  ([#425](https://github.com/n24q02m/better-telegram-mcp/pull/425),
  [`72b2da9`](https://github.com/n24q02m/better-telegram-mcp/commit/72b2da933d98fa72e574e459413f9f76d097bdee))


## v4.9.0-beta.1 (2026-04-30)

### Features

- Route stdio mode to FastMCP direct + multi-target Dockerfile
  ([#424](https://github.com/n24q02m/better-telegram-mcp/pull/424),
  [`e174f90`](https://github.com/n24q02m/better-telegram-mcp/commit/e174f90afd281b7a2a897c9c633677287b111d96))


## v4.8.5 (2026-04-29)

### Bug Fixes

- Bump n24q02m-mcp-core to 1.11.3 for D17 tools cache refresh
  ([#418](https://github.com/n24q02m/better-telegram-mcp/pull/418),
  [`1c0fb63`](https://github.com/n24q02m/better-telegram-mcp/commit/1c0fb63437745b1a056e01af5f13efa2d4941447))

- Pin @latest in plugin.json to bypass uvx cache stale versions
  ([#416](https://github.com/n24q02m/better-telegram-mcp/pull/416),
  [`0caf1a6`](https://github.com/n24q02m/better-telegram-mcp/commit/0caf1a6d76870fa7bd78ec34523902d86ca4a7a2))

- Rebuild uv.lock without local path source
  ([#416](https://github.com/n24q02m/better-telegram-mcp/pull/416),
  [`0caf1a6`](https://github.com/n24q02m/better-telegram-mcp/commit/0caf1a6d76870fa7bd78ec34523902d86ca4a7a2))


## v4.8.4 (2026-04-29)

### Bug Fixes

- Rebuild uv.lock without local path source
  ([#414](https://github.com/n24q02m/better-telegram-mcp/pull/414),
  [`ab5433a`](https://github.com/n24q02m/better-telegram-mcp/commit/ab5433ac7dbb391ec562e095deb19ad4cae14625))


## v4.8.3 (2026-04-29)

### Bug Fixes

- Improve credential form accessibility with ARIA refinements
  ([#409](https://github.com/n24q02m/better-telegram-mcp/pull/409),
  [`f3e21ac`](https://github.com/n24q02m/better-telegram-mcp/commit/f3e21ac8cd3a76979e61da2600e14487d43b83d2))

- Register config__open_relay tool (Transparent Bridge Wave 3)
  ([#412](https://github.com/n24q02m/better-telegram-mcp/pull/412),
  [`cd865ea`](https://github.com/n24q02m/better-telegram-mcp/commit/cd865ead4aa79157a09e253050b3a4127464d821))

- Switch plugin.json to stdio proxy for local relay testing
  ([#410](https://github.com/n24q02m/better-telegram-mcp/pull/410),
  [`b7d93d0`](https://github.com/n24q02m/better-telegram-mcp/commit/b7d93d00c2f79006b5775f9833aa59401f4b865c))

- **deps**: Bump n24q02m-mcp-core to 1.10.0 — Transparent Bridge waves 1-3
  ([#410](https://github.com/n24q02m/better-telegram-mcp/pull/410),
  [`b7d93d0`](https://github.com/n24q02m/better-telegram-mcp/commit/b7d93d00c2f79006b5775f9833aa59401f4b865c))


## v4.8.2 (2026-04-28)

### Bug Fixes

- Migrate plugin.json to deployed HTTP remote + add /health route
  ([#406](https://github.com/n24q02m/better-telegram-mcp/pull/406),
  [`96be424`](https://github.com/n24q02m/better-telegram-mcp/commit/96be424a98f11501dffed9da9b1fa80019e1fb8d))

- Replace stale OAuth 2.1 wording with DCR + relay form in setup-manual
  ([#405](https://github.com/n24q02m/better-telegram-mcp/pull/405),
  [`fd717a6`](https://github.com/n24q02m/better-telegram-mcp/commit/fd717a66ff2831b7387f6e76a0af45254567e0b1))

- **deps**: Bump n24q02m-mcp-core to 1.10.0 — Transparent Bridge waves 1-3
  ([#408](https://github.com/n24q02m/better-telegram-mcp/pull/408),
  [`044b56f`](https://github.com/n24q02m/better-telegram-mcp/commit/044b56fe10033ab7a82a24b8fbf19949e7bc08b7))


## v4.8.1 (2026-04-28)

### Bug Fixes

- Bump n24q02m-mcp-core to 1.9.0 ([#404](https://github.com/n24q02m/better-telegram-mcp/pull/404),
  [`1a7db20`](https://github.com/n24q02m/better-telegram-mcp/commit/1a7db200b41e9737906b8878eb02dc97ea823fbe))

- **deps**: Update non-major dependencies
  ([#401](https://github.com/n24q02m/better-telegram-mcp/pull/401),
  [`c7ac9af`](https://github.com/n24q02m/better-telegram-mcp/commit/c7ac9afe8221210aad1b880bfa0067734e35d63f))


## v4.8.0 (2026-04-27)

### Bug Fixes

- Bump n24q02m-mcp-core to 1.8.0 + widen pydantic to <2.14
  ([#399](https://github.com/n24q02m/better-telegram-mcp/pull/399),
  [`291c7c2`](https://github.com/n24q02m/better-telegram-mcp/commit/291c7c2cb5e434ae11a6e954cc1ddcdd911ba4ad))

- Clear resolved 2026-04-18 known bugs from CLAUDE.md
  ([#397](https://github.com/n24q02m/better-telegram-mcp/pull/397),
  [`5b5aeee`](https://github.com/n24q02m/better-telegram-mcp/commit/5b5aeeee3c536e726c0ab3e60cd4e0c0d20af93d))

- Clear resolved 2026-04-18 known bugs from CLAUDE.md
  ([#396](https://github.com/n24q02m/better-telegram-mcp/pull/396),
  [`389b0b0`](https://github.com/n24q02m/better-telegram-mcp/commit/389b0b096d46605522ee56ea2c687ffe54caa308))

### Features

- Add ## E2E section to CLAUDE.md per Task 21 docs rollout
  ([#395](https://github.com/n24q02m/better-telegram-mcp/pull/395),
  [`da53a65`](https://github.com/n24q02m/better-telegram-mcp/commit/da53a65dbab24fc731869fb560c1c518882ec5ab))

- Render bot token + phone with prefilled value attrs
  ([#397](https://github.com/n24q02m/better-telegram-mcp/pull/397),
  [`5b5aeee`](https://github.com/n24q02m/better-telegram-mcp/commit/5b5aeeee3c536e726c0ab3e60cd4e0c0d20af93d))


## v4.7.2-beta.1 (2026-04-27)

### Bug Fixes

- Sweep doppler/infisical refs to skret SSM
  ([`1d3a948`](https://github.com/n24q02m/better-telegram-mcp/commit/1d3a9489a5db389b3c15a532652842a410f04cdc))


## v4.7.1 (2026-04-24)

### Bug Fixes

- Regenerate uv.lock without [tool.uv.sources] for Docker build
  ([#388](https://github.com/n24q02m/better-telegram-mcp/pull/388),
  [`f7e7ca4`](https://github.com/n24q02m/better-telegram-mcp/commit/f7e7ca47911c729089043639b7109f9a0f6f23a5))


## v4.7.0 (2026-04-24)

### Bug Fixes

- Bump n24q02m-mcp-core to 1.7.5 + loosen pydantic for cohere compat
  ([#385](https://github.com/n24q02m/better-telegram-mcp/pull/385),
  [`e09b1f6`](https://github.com/n24q02m/better-telegram-mcp/commit/e09b1f6cb3730555620f985cb57bf9e1369d0c16))

- Bump n24q02m-mcp-core to 1.7.6 ([#387](https://github.com/n24q02m/better-telegram-mcp/pull/387),
  [`f555bf1`](https://github.com/n24q02m/better-telegram-mcp/commit/f555bf192c85fb3872474a2c08ebb3484d49de5a))

- Bump n24q02m-mcp-core to >=1.7.0 ([#379](https://github.com/n24q02m/better-telegram-mcp/pull/379),
  [`1a1ae4e`](https://github.com/n24q02m/better-telegram-mcp/commit/1a1ae4e6a8139882859e7ea19ce6ff9f60eb2239))

- Optimize trusted proxy list lookup to O(1) (PR 374 split)
  ([`407539f`](https://github.com/n24q02m/better-telegram-mcp/commit/407539fd79c46a1fa9b0cf233703c368244644d2))

- **deps**: Update dependency uvicorn to >=0.46.0
  ([#375](https://github.com/n24q02m/better-telegram-mcp/pull/375),
  [`0e17be6`](https://github.com/n24q02m/better-telegram-mcp/commit/0e17be6d8414287a0f87870e323206c9e1deb9a8))

### Chores

- **deps**: Update python:3.13-slim-bookworm docker digest to bb73517
  ([#372](https://github.com/n24q02m/better-telegram-mcp/pull/372),
  [`2fe0dcc`](https://github.com/n24q02m/better-telegram-mcp/commit/2fe0dcc713ba13ce4786bc5715e65ac2dd57f931))

### Features

- Enforce Smart Daemon Manager (1-Daemon) for stdio transport
  ([`8d68f2e`](https://github.com/n24q02m/better-telegram-mcp/commit/8d68f2e19ef239ac769b0baf7306fc9182e0c252))


## v4.6.12-beta.1 (2026-04-22)

### Bug Fixes

- Add RFC 7591 dynamic client registration endpoint
  ([`ee5d1aa`](https://github.com/n24q02m/better-telegram-mcp/commit/ee5d1aad8e838a9c95bfbe22cdc24eb9aa790a1d))


## v4.6.11 (2026-04-22)

### Bug Fixes

- Return 401 + WWW-Authenticate for bearer auth failures
  ([#370](https://github.com/n24q02m/better-telegram-mcp/pull/370),
  [`a23ea71`](https://github.com/n24q02m/better-telegram-mcp/commit/a23ea71b093f67f50de51ffe49403fb1189271e0))


## v4.6.10 (2026-04-22)

### Bug Fixes

- Follow redirect_url after async OTP/password completion
  ([#369](https://github.com/n24q02m/better-telegram-mcp/pull/369),
  [`0560529`](https://github.com/n24q02m/better-telegram-mcp/commit/0560529f5700849f46438e8e74c35638ef657d30))


## v4.6.9 (2026-04-22)

### Bug Fixes

- Bump n24q02m-mcp-core to 1.6.3 (relay form follow redirect_url)
  ([#368](https://github.com/n24q02m/better-telegram-mcp/pull/368),
  [`e61e041`](https://github.com/n24q02m/better-telegram-mcp/commit/e61e0418b707b0bd3f0b68be85f97e5af8d2cfba))


## v4.6.8 (2026-04-22)

### Bug Fixes

- Bump mcp-core to 1.6.2 ([#366](https://github.com/n24q02m/better-telegram-mcp/pull/366),
  [`09d2fab`](https://github.com/n24q02m/better-telegram-mcp/commit/09d2fabb3cf07cab1f1b2a91eb22051f03f1bced))


## v4.6.7 (2026-04-22)

### Bug Fixes

- Bump n24q02m-mcp-core to 1.5.1
  ([`863260d`](https://github.com/n24q02m/better-telegram-mcp/commit/863260d3b811c4ae7318262b49280eca07ab5050))

- Bump n24q02m-mcp-core to 1.6.1 ([#364](https://github.com/n24q02m/better-telegram-mcp/pull/364),
  [`4630fa8`](https://github.com/n24q02m/better-telegram-mcp/commit/4630fa890a406cc2c79c464468c92af3c0a0fcbe))

- **deps**: Update non-major dependencies
  ([#358](https://github.com/n24q02m/better-telegram-mcp/pull/358),
  [`6d53224`](https://github.com/n24q02m/better-telegram-mcp/commit/6d5322438b3bb8c2e80547ce9a232f7f0487c5a9))

### Chores

- **deps**: Lock file maintenance ([#360](https://github.com/n24q02m/better-telegram-mcp/pull/360),
  [`65d9888`](https://github.com/n24q02m/better-telegram-mcp/commit/65d9888dd78220e004abb18f0e2afe043f3a82fb))

- **deps**: Update astral-sh/setup-uv action to v8
  ([#359](https://github.com/n24q02m/better-telegram-mcp/pull/359),
  [`3ff3cb7`](https://github.com/n24q02m/better-telegram-mcp/commit/3ff3cb759bef04ec263e13093b554d2df38f030b))


## v4.6.6 (2026-04-21)

### Bug Fixes

- Add aria-busy spinner to credential form submit button
  ([`43f6eed`](https://github.com/n24q02m/better-telegram-mcp/commit/43f6eed7495546a5962dd2d9b7e55126632bc4c7))

- Bump non-major Python deps (lock file maintenance)
  ([`a405714`](https://github.com/n24q02m/better-telegram-mcp/commit/a405714ed0625c4f8a4c73edc27b6a515bbafffa))

- Bump non-major Python deps incl mcp-core to 1.5.0
  ([`a4ea367`](https://github.com/n24q02m/better-telegram-mcp/commit/a4ea367ecc157c90bd4287bcacaae3a8626dacfa))

- Bump step-security/harden-runner digest to 8d3c67d
  ([`95b1036`](https://github.com/n24q02m/better-telegram-mcp/commit/95b10364cee8ee3cf02029abc889cf48d61ab068))


## v4.6.5 (2026-04-21)

### Bug Fixes

- Route HTTP entry through transports.http so multi-user OAuth actually runs
  ([`9821675`](https://github.com/n24q02m/better-telegram-mcp/commit/982167513eea5e4c408cbad4fdc0230bb68ede95))


## v4.6.4 (2026-04-21)

### Bug Fixes

- Accept Settings api_id/api_hash defaults for multi-user mode detection
  ([`6d32d4e`](https://github.com/n24q02m/better-telegram-mcp/commit/6d32d4e8997e413928573a620af81897c59ee814))


## v4.6.3 (2026-04-21)

### Bug Fixes

- Case-insensitive Bearer token parsing per RFC 7235 (with tests)
  ([`411ae2d`](https://github.com/n24q02m/better-telegram-mcp/commit/411ae2daced4a010b468db87028a99136f57beac))

- Improve OTP and 2FA password form accessibility
  ([`0ceacf3`](https://github.com/n24q02m/better-telegram-mcp/commit/0ceacf39ee6598ef5c38f6202a6c500526e39b01))

- Memoize trusted proxy parsing in hot path
  ([`4065522`](https://github.com/n24q02m/better-telegram-mcp/commit/40655220289f90ce1bbd0b99010277f8ca967bfe))

- Refuse public-URL single-user fallback + propagate SubjectContext
  ([`4fb18e3`](https://github.com/n24q02m/better-telegram-mcp/commit/4fb18e30798c218fe9b8c263c778e4f66f35fddc))

- Stdio fallback renders custom telegram credential form
  ([`1142286`](https://github.com/n24q02m/better-telegram-mcp/commit/114228637e3e03cd21dda2dbbda60c8029494fd8))

- Stdio fallback spawns local credential form, not remote relay
  ([`48f338b`](https://github.com/n24q02m/better-telegram-mcp/commit/48f338bd252a8c9716d5440697b8aa42f239c62f))

- **deps**: Lock file maintenance (filelock 3.28.0->3.29.0)
  ([`d0f1865`](https://github.com/n24q02m/better-telegram-mcp/commit/d0f18658f332546dc9e921fd6805406b970d2ae4))


## v4.6.2 (2026-04-20)

### Bug Fixes

- Bump n24q02m-mcp-core to >=1.4.3 (aria-busy step reset parity)
  ([#350](https://github.com/n24q02m/better-telegram-mcp/pull/350),
  [`df06f1a`](https://github.com/n24q02m/better-telegram-mcp/commit/df06f1adc364ec52ec4ab1d7dcb0ef93c7bc19e5))

- Clear aria-busy on step-input reset to unblock 2FA submit
  ([#348](https://github.com/n24q02m/better-telegram-mcp/pull/348),
  [`eb1993f`](https://github.com/n24q02m/better-telegram-mcp/commit/eb1993fd8cccf34bbe9ef837274f7640f44ef69b))


## v4.6.1 (2026-04-20)

### Bug Fixes

- Bump n24q02m-mcp-core to >=1.4.2 ([#347](https://github.com/n24q02m/better-telegram-mcp/pull/347),
  [`82bdc1d`](https://github.com/n24q02m/better-telegram-mcp/commit/82bdc1d8c80b26e3d9d9479cea650aa54478d575))


## v4.6.0 (2026-04-19)

### Bug Fixes

- Bump mcp-core to 1.3.0 ([#335](https://github.com/n24q02m/better-telegram-mcp/pull/335),
  [`51eeaed`](https://github.com/n24q02m/better-telegram-mcp/commit/51eeaeda5c2092a2d09982ee65a0dea6318a323e))

- Bump n24q02m-mcp-core to 1.4.0 ([#340](https://github.com/n24q02m/better-telegram-mcp/pull/340),
  [`5de8bdc`](https://github.com/n24q02m/better-telegram-mcp/commit/5de8bdcb059a6b22916fa55726e20b9eaeb72557))

- **deps**: Update dependency pydantic to >=2.13.2
  ([#329](https://github.com/n24q02m/better-telegram-mcp/pull/329),
  [`ab699f4`](https://github.com/n24q02m/better-telegram-mcp/commit/ab699f404ee316f529cf23a2409c386244d9c8ba))

### Chores

- Log non-critical exceptions in UserBackend
  ([#315](https://github.com/n24q02m/better-telegram-mcp/pull/315),
  [`696dddf`](https://github.com/n24q02m/better-telegram-mcp/commit/696dddfe7e94d215653b35ffdf5b57e77b8da789))

- **deps**: Lock file maintenance ([#330](https://github.com/n24q02m/better-telegram-mcp/pull/330),
  [`cd86b41`](https://github.com/n24q02m/better-telegram-mcp/commit/cd86b410dfbe1ad61e5885e7f9542838b6c088e5))

- **deps**: Update step-security/harden-runner digest to 6c3c2f2
  ([#328](https://github.com/n24q02m/better-telegram-mcp/pull/328),
  [`8bda093`](https://github.com/n24q02m/better-telegram-mcp/commit/8bda0936c55d612aa3dbe115db43f3244a537694))

### Performance Improvements

- **user-backend**: Move blocking file I/O to background threads
  ([#320](https://github.com/n24q02m/better-telegram-mcp/pull/320),
  [`4f4f9d4`](https://github.com/n24q02m/better-telegram-mcp/commit/4f4f9d45b26e86fc686021960d1d3aa27fab16db))

### Testing

- Add unit tests for AuthClient and enable coverage reporting
  ([#271](https://github.com/n24q02m/better-telegram-mcp/pull/271),
  [`457f4ee`](https://github.com/n24q02m/better-telegram-mcp/commit/457f4ee68bca2b9a0b29643ed0a06adf1b0eb436))

- **transports**: Add coverage for http_multi_user.py
  ([#318](https://github.com/n24q02m/better-telegram-mcp/pull/318),
  [`61dc43a`](https://github.com/n24q02m/better-telegram-mcp/commit/61dc43a5d1f58dc31a5620c8b47ffd85fa167b09))


## v4.6.0-beta.1 (2026-04-18)

### Bug Fixes

- Add tests for user-mode OTP/2FA relay branches + fix Python 3.13 variable shadowing bug
  ([#334](https://github.com/n24q02m/better-telegram-mcp/pull/334),
  [`a0b5ba5`](https://github.com/n24q02m/better-telegram-mcp/commit/a0b5ba50ec489a6781a903f00b5c1ece2e942829))

- Apply ruff format to auth + test files for CI parity
  ([#334](https://github.com/n24q02m/better-telegram-mcp/pull/334),
  [`a0b5ba5`](https://github.com/n24q02m/better-telegram-mcp/commit/a0b5ba50ec489a6781a903f00b5c1ece2e942829))

- Mask sensitive token in auth server start log
  ([#313](https://github.com/n24q02m/better-telegram-mcp/pull/313),
  [`2c2571c`](https://github.com/n24q02m/better-telegram-mcp/commit/2c2571c741b5b16016ce638c0409f16b0bd113f8))

- Remove hardcoded default dev secret and centralize secret management
  ([#312](https://github.com/n24q02m/better-telegram-mcp/pull/312),
  [`b335f7d`](https://github.com/n24q02m/better-telegram-mcp/commit/b335f7db8535a3fcf5e84eeb94f9e4a7282e8e5b))

- Remove sensitive auth session URL from logs
  ([#307](https://github.com/n24q02m/better-telegram-mcp/pull/307),
  [`137e743`](https://github.com/n24q02m/better-telegram-mcp/commit/137e743749c5d14f634f79997fb7dab1f28e5f69))

- **auth**: Log swallowed exception in pending OTP disconnect
  ([#317](https://github.com/n24q02m/better-telegram-mcp/pull/317),
  [`9374e4c`](https://github.com/n24q02m/better-telegram-mcp/commit/9374e4cb2c21c5b1bd01cbf372faec962264b5f4))

### Features

- Fix user-mode OTP flow over remote relay and patch bot token leak
  ([#334](https://github.com/n24q02m/better-telegram-mcp/pull/334),
  [`a0b5ba5`](https://github.com/n24q02m/better-telegram-mcp/commit/a0b5ba50ec489a6781a903f00b5c1ece2e942829))

### Performance Improvements

- **auth**: Optimize stale OTP cleanup
  ([#306](https://github.com/n24q02m/better-telegram-mcp/pull/306),
  [`e37683d`](https://github.com/n24q02m/better-telegram-mcp/commit/e37683d2eb4b1ae4c4a6e1b03b003159dd4a0977))

### Testing

- Add relay_schema.py tests and fix ty check failures
  ([#266](https://github.com/n24q02m/better-telegram-mcp/pull/266),
  [`b94dd81`](https://github.com/n24q02m/better-telegram-mcp/commit/b94dd81c64176e829cc6603bcd0bb768d520fa5b))

- Add unit tests for auth_client.py and remove from coverage omit
  ([#300](https://github.com/n24q02m/better-telegram-mcp/pull/300),
  [`b286b83`](https://github.com/n24q02m/better-telegram-mcp/commit/b286b836a17387d0b884de2c2e123925f49301b2))

- Add unit tests for http transport and enable coverage
  ([#304](https://github.com/n24q02m/better-telegram-mcp/pull/304),
  [`f6e5868`](https://github.com/n24q02m/better-telegram-mcp/commit/f6e58683bfa22017e20b6ff7f9cfb920335d0165))

- Add unit tests for oauth_server transport
  ([#303](https://github.com/n24q02m/better-telegram-mcp/pull/303),
  [`f48fd99`](https://github.com/n24q02m/better-telegram-mcp/commit/f48fd99d94fcfd132e82897e1b6c8be274e863fd))


## v4.5.3 (2026-04-17)

### Bug Fixes

- Bump n24q02m-mcp-core to 1.2.0 (authlib CVE patch)
  ([`ff8cbd4`](https://github.com/n24q02m/better-telegram-mcp/commit/ff8cbd41eea8de1d38eea633c581fecaa4bf1765))

- Upgrade authlib to 1.6.11 (CVE-2024-cross-site-request-forging)
  ([`591a986`](https://github.com/n24q02m/better-telegram-mcp/commit/591a9862365524dd261a826c91d882f1056d98b7))


## v4.5.2 (2026-04-17)

### Bug Fixes

- Update lockfile to include mcp-core 1.1.1
  ([`23e1dfc`](https://github.com/n24q02m/better-telegram-mcp/commit/23e1dfc090c1e307f2d4867bad5166365c13961f))


## v4.5.1 (2026-04-17)

### Bug Fixes

- Bump version to rebuild with mcp-core 1.1.1
  ([`0565a92`](https://github.com/n24q02m/better-telegram-mcp/commit/0565a92bac6f3ebccb4b800d097a347a67cd5358))


## v4.5.0 (2026-04-17)

### Bug Fixes

- Add diacritic preservation pre-commit hook
  ([#324](https://github.com/n24q02m/better-telegram-mcp/pull/324),
  [`97351c9`](https://github.com/n24q02m/better-telegram-mcp/commit/97351c97ef3a1737eff97e0f1ec4d51a527802c8))

- Bump authlib to 1.6.11 for CSRF cache bypass (GHSA-jj8c-mmj3-mmgv)
  ([`874aad3`](https://github.com/n24q02m/better-telegram-mcp/commit/874aad31fff05b23089ac49b44d28c8fc1a1c5b6))

- Document live remote URL for HTTP multi-user setup
  ([#323](https://github.com/n24q02m/better-telegram-mcp/pull/323),
  [`15c6c57`](https://github.com/n24q02m/better-telegram-mcp/commit/15c6c57f822eb97c4b234fc947dfc9af898fb362))

- Ignore coverage.xml and htmlcov artifacts
  ([#323](https://github.com/n24q02m/better-telegram-mcp/pull/323),
  [`15c6c57`](https://github.com/n24q02m/better-telegram-mcp/commit/15c6c57f822eb97c4b234fc947dfc9af898fb362))

- Ignore coverage.xml and htmlcov artifacts
  ([`53779fa`](https://github.com/n24q02m/better-telegram-mcp/commit/53779fab745eb62e2d8b9ec4bf3d924578f9ac2c))

- Replace swallowed exceptions with logging in credential_state
  ([`e40cae7`](https://github.com/n24q02m/better-telegram-mcp/commit/e40cae7104834cd3c9df88bce0ddd03fabd865f2))

- **deps**: Bump actions/create-github-app-token digest to 1b10c78
  ([#289](https://github.com/n24q02m/better-telegram-mcp/pull/289),
  [`c79c1d0`](https://github.com/n24q02m/better-telegram-mcp/commit/c79c1d06aadc93dc9c883700ddc0b9347cd0e195))

- **deps**: Bump actions/upload-artifact digest to 043fb46
  ([#278](https://github.com/n24q02m/better-telegram-mcp/pull/278),
  [`ddba3fc`](https://github.com/n24q02m/better-telegram-mcp/commit/ddba3fc7982fb8bf67919059527b93663c816ed2))

- **deps**: Bump docker/build-push-action digest to bcafcac
  ([#290](https://github.com/n24q02m/better-telegram-mcp/pull/290),
  [`5e6fe0e`](https://github.com/n24q02m/better-telegram-mcp/commit/5e6fe0e33798660ee63bba3f4b96a05eb99c2102))

- **deps**: Bump non-major dependencies
  ([#291](https://github.com/n24q02m/better-telegram-mcp/pull/291),
  [`8cdfdc9`](https://github.com/n24q02m/better-telegram-mcp/commit/8cdfdc9a65882508301de13264be69bc9cff13e0))

- **deps**: Lock file maintenance ([#292](https://github.com/n24q02m/better-telegram-mcp/pull/292),
  [`14684e5`](https://github.com/n24q02m/better-telegram-mcp/commit/14684e52b0570031c888eac89c4b50d1159b1540))

### Features

- Add accessible CSS spinners for async loading states in credential form
  ([#295](https://github.com/n24q02m/better-telegram-mcp/pull/295),
  [`84c00b7`](https://github.com/n24q02m/better-telegram-mcp/commit/84c00b74347b9d94a6d3cf20cc9cd690c9c6cbb5))

- Cache trusted_proxy_list using functools.cached_property
  ([`484cbd7`](https://github.com/n24q02m/better-telegram-mcp/commit/484cbd7bfdcf94251f8dc792d3e168b9f6d7944a))

- Optimize OTP cleanup traversal with chronological early-exit
  ([#296](https://github.com/n24q02m/better-telegram-mcp/pull/296),
  [`db23fe3`](https://github.com/n24q02m/better-telegram-mcp/commit/db23fe357027ebebde5c68940637908199eff5dd))

- Use semantic forms for auth UI
  ([`b819ee1`](https://github.com/n24q02m/better-telegram-mcp/commit/b819ee1e9ef2b5ac75a1156a4455f4713db6173f))


## v4.4.2 (2026-04-17)

### Bug Fixes

- Forward PORT env var to run_http in main()
  ([`a34c2c4`](https://github.com/n24q02m/better-telegram-mcp/commit/a34c2c46935dfaa159b13aa7c58017ad8abf7116))


## v4.4.1 (2026-04-17)

### Bug Fixes

- Bump mcp-core pin to 1.1.0 and forward HOST env to run_local_server
  ([`c9e809f`](https://github.com/n24q02m/better-telegram-mcp/commit/c9e809f4cd711919b41d0b6be7fb67f83a4b36cd))

### Chores

- Ignore AI assistant traces
  ([`e94643d`](https://github.com/n24q02m/better-telegram-mcp/commit/e94643dba139edcee9e5e64ae4142f850c2a7ef4))


## v4.4.0 (2026-04-13)

### Bug Fixes

- Add cryptg dependency for Telethon MTProto decryption
  ([`884662c`](https://github.com/n24q02m/better-telegram-mcp/commit/884662cc34c7367ed013faa8d52751a399cc313d))

- Add missing config setup actions to README
  ([`a6c0f65`](https://github.com/n24q02m/better-telegram-mcp/commit/a6c0f6584c05299abbfaef38ab71f468aa583e03))

- Add tests for UserBackend.sign_in chmod path
  ([#270](https://github.com/n24q02m/better-telegram-mcp/pull/270),
  [`fd019fa`](https://github.com/n24q02m/better-telegram-mcp/commit/fd019fadcffd4e596257ae455cab233ab2f2f58c))

- Block sensitive paths on macOS firmlinks
  ([`82ba023`](https://github.com/n24q02m/better-telegram-mcp/commit/82ba023f9eea829320891010e2f5a60ad725032d))

- Bump n24q02m-mcp-core to >=1.0.0 stable
  ([`1ac3c06`](https://github.com/n24q02m/better-telegram-mcp/commit/1ac3c06b1e3d3ed5464d5743a845c0da908fd752))

- Cache static help docs in memory
  ([`04f6954`](https://github.com/n24q02m/better-telegram-mcp/commit/04f695429ee7488df096536c4f06ca41b96024b1))

- Drop local uv.sources override for n24q02m-mcp-core
  ([`eccb4bd`](https://github.com/n24q02m/better-telegram-mcp/commit/eccb4bd8a6e8923281a732d599e7969f05cce386))

- Flatten relay_schema for mcp-core credential form rendering
  ([`33f9821`](https://github.com/n24q02m/better-telegram-mcp/commit/33f98211c9b1cc1ae41fa430145dac3342b6c9a1))

- Improve relay UX when Telethon session already authorized
  ([`0dc0fdb`](https://github.com/n24q02m/better-telegram-mcp/commit/0dc0fdbb5b43738f31faa6c24d441f12b61527eb))

- Lock file maintenance
  ([`91a089d`](https://github.com/n24q02m/better-telegram-mcp/commit/91a089df716dc5bc7b28bc2f559ef017a4510fa7))

- Make credential callbacks async to avoid running-loop error
  ([`bdb5a52`](https://github.com/n24q02m/better-telegram-mcp/commit/bdb5a5242f0a3a394c23c813857ecc7c917f9381))

- Remove dead relay-based OTP flow replaced by /otp endpoint
  ([`85d8204`](https://github.com/n24q02m/better-telegram-mcp/commit/85d8204bb1b526c4da6e40abf27ba42cde0f6a92))

- Remove stale ty ignore directives after type inference improvements
  ([`d290442`](https://github.com/n24q02m/better-telegram-mcp/commit/d2904420c25e8939d9596023fed7da90fd99b02a))

- Unblock CI install by removing editable mcp-relay-core source
  ([`8ace5bf`](https://github.com/n24q02m/better-telegram-mcp/commit/8ace5bfffebbee08852f442c6db6cebd8cf027a5))

- Update non-major dependencies
  ([`93f721b`](https://github.com/n24q02m/better-telegram-mcp/commit/93f721b2173a69f8fe5d54c9e85b2e592df21d1d))

- Update python:3.13-slim-bookworm docker digest to 061b6e5
  ([`9de3fcb`](https://github.com/n24q02m/better-telegram-mcp/commit/9de3fcb449d6c6915daa2429d834a290f9b2ee68))

- Update step-security/harden-runner digest to f808768
  ([`aba2946`](https://github.com/n24q02m/better-telegram-mcp/commit/aba2946a8cb4b79376bf338758b3d76399a935db))

- User mode returns info next_step instead of immediate complete
  ([`b14078d`](https://github.com/n24q02m/better-telegram-mcp/commit/b14078d6d28d613e59afae4861c0e11e32d67e43))

- **deps**: Update non-major dependencies
  ([#250](https://github.com/n24q02m/better-telegram-mcp/pull/250),
  [`a97470e`](https://github.com/n24q02m/better-telegram-mcp/commit/a97470e20314ef233ba824666a96855f91ade079))

### Chores

- **deps**: Bump cryptography in the uv group across 1 directory
  ([#254](https://github.com/n24q02m/better-telegram-mcp/pull/254),
  [`36ec398`](https://github.com/n24q02m/better-telegram-mcp/commit/36ec398f477f09e86a9b13e68e64367305fdd6d6))

- **deps**: Lock file maintenance ([#251](https://github.com/n24q02m/better-telegram-mcp/pull/251),
  [`93cbd5a`](https://github.com/n24q02m/better-telegram-mcp/commit/93cbd5a6af44656ebbda5fbf959852295e70d9f4))

- **deps**: Update dependency cryptography to v46.0.7 [security]
  ([#256](https://github.com/n24q02m/better-telegram-mcp/pull/256),
  [`c7ec0b3`](https://github.com/n24q02m/better-telegram-mcp/commit/c7ec0b324c89647cca86ec0a6819b2ecb0202315))

### Features

- Add cross-OS CI matrix (ubuntu/windows/macos)
  ([`89d5534`](https://github.com/n24q02m/better-telegram-mcp/commit/89d5534f702a169d87d65587d10cceb0d28cfa14))

- Add on_step_submitted for multi-step OTP via /otp endpoint
  ([`79b0041`](https://github.com/n24q02m/better-telegram-mcp/commit/79b0041d1c0911f8eb2422ca570c96a18ad29d81))

- Default to HTTP transport, --stdio for backward compat
  ([`afe5973`](https://github.com/n24q02m/better-telegram-mcp/commit/afe5973eeedda6e9fc29779a6851705d7796bac1))

- Hot-reload backend after relay credentials are configured
  ([`c94314d`](https://github.com/n24q02m/better-telegram-mcp/commit/c94314d1b0eed69daef22fcb1f8efa1d48bea76a))

- Migrate from mcp-relay-core to mcp-core
  ([`a88004a`](https://github.com/n24q02m/better-telegram-mcp/commit/a88004a6d69be5a8018180f0d5e4da4c3706f12a))

- Migrate to mcp-core Self-hosted AS for HTTP default
  ([`cf1d209`](https://github.com/n24q02m/better-telegram-mcp/commit/cf1d209d4a12eeb430d902ce54534e8c8324f410))

- Restore telegram credential form with Bot/User mode tabs
  ([`eaac8a6`](https://github.com/n24q02m/better-telegram-mcp/commit/eaac8a65bff50ba421b4dd211b55052ada3d4f5b))

- Sync local changes and implement OAuth hot-reload
  ([`4861941`](https://github.com/n24q02m/better-telegram-mcp/commit/48619417af5a346c2bc7a91fd28f512314525224))

- **auth**: Add aria-live regions to status messages
  ([#170](https://github.com/n24q02m/better-telegram-mcp/pull/170),
  [`1b150fc`](https://github.com/n24q02m/better-telegram-mcp/commit/1b150fc84534a47bab3a214b80c6a7d2ce2a72e4))


## v4.3.0 (2026-04-07)

### Bug Fixes

- Add credential state tests for relay redesign
  ([`6d72698`](https://github.com/n24q02m/better-telegram-mcp/commit/6d726989ee2f2a809428ff60df016a637b29087a))

- Apply ruff formatting to credential state tests
  ([`ed98dac`](https://github.com/n24q02m/better-telegram-mcp/commit/ed98dacf1d66dedfd7e388e77fca558191222f1b))

- PBKDF2 600k iterations and random salt migration in session store
  ([`48987f3`](https://github.com/n24q02m/better-telegram-mcp/commit/48987f38fe3a5144c90cd67f75bbe251667ff28e))

- Remove BETA markers and promote relay as primary setup method
  ([`c8c05fa`](https://github.com/n24q02m/better-telegram-mcp/commit/c8c05fa79edb42257184671b67a6e06d1447d55e))

- Resolve ruff lint errors in credential state tests
  ([`1a5a374`](https://github.com/n24q02m/better-telegram-mcp/commit/1a5a374d37109ad28102b9397a030006588dccc6))

- Sync uv.lock with current version
  ([`328705f`](https://github.com/n24q02m/better-telegram-mcp/commit/328705fe3abab4ce64c2437f25b032e85bc5c533))

### Features

- Migrate code review from Qodo to CodeRabbit
  ([#211](https://github.com/n24q02m/better-telegram-mcp/pull/211),
  [`065e50d`](https://github.com/n24q02m/better-telegram-mcp/commit/065e50dbd61b956d370f7722dc19b9e4b7ba3d5b))


## v4.3.0-beta.1 (2026-04-07)

### Features

- Add setup actions to config tool for relay trigger
  ([`0bb2979`](https://github.com/n24q02m/better-telegram-mcp/commit/0bb2979b699345da5441975d7e08cc18663aace1))


## v4.2.0 (2026-04-06)

### Bug Fixes

- Mark relay as BETA, promote env vars as primary setup method
  ([`756bf22`](https://github.com/n24q02m/better-telegram-mcp/commit/756bf223c32f6c76a39c27b0555a22723ea6b95a))

### Features

- Non-blocking relay with state machine and lazy trigger
  ([`567f08a`](https://github.com/n24q02m/better-telegram-mcp/commit/567f08ab22f9c5999a2e0f50de863d3c10fd5c9f))


## v4.1.0 (2026-04-04)

### Bug Fixes

- CSRF token protection, auth_server tests, dependency updates, and test improvements
  ([#169](https://github.com/n24q02m/better-telegram-mcp/pull/169),
  [`1f743de`](https://github.com/n24q02m/better-telegram-mcp/commit/1f743de1a8cad73bd835cb8fefeb70c5c9cdc132))

### Features

- Add agent/manual setup guides, simplify README, cleanup root
  ([`1dad3c9`](https://github.com/n24q02m/better-telegram-mcp/commit/1dad3c9ea91b4e5517d4274bc6cd81477ad30b8e))


## v4.0.1 (2026-04-03)

### Bug Fixes

- Consolidated security fixes, dependency updates, and test improvements
  ([#135](https://github.com/n24q02m/better-telegram-mcp/pull/135),
  [`07ad289`](https://github.com/n24q02m/better-telegram-mcp/commit/07ad289ea120d3965139040e34564a108f04685a))

- Scope marketplace sync token to claude-plugins repo
  ([`4e83bdb`](https://github.com/n24q02m/better-telegram-mcp/commit/4e83bdb6dc3a5a30caad2e6a1a5ba75c9f3432d0))


## v4.0.0 (2026-04-03)

### Bug Fixes

- HTTP single-user mode respects env vars before CredentialStore
  ([`4a88149`](https://github.com/n24q02m/better-telegram-mcp/commit/4a881490a186825ceb84d28901d9ab308aad93a5))

### Documentation

- Fix tool names in README to match server.py (singular form)
  ([`f13241a`](https://github.com/n24q02m/better-telegram-mcp/commit/f13241a3eab3648d0e955f428fc0fae7ecc808d8))

### Features

- Implement multi-user HTTP MCP endpoint with per-user backend isolation
  ([`eb76960`](https://github.com/n24q02m/better-telegram-mcp/commit/eb76960c2d372f516bf286aa723122faae9ccf4c))

- Remove deprecated Gemini CLI extension support
  ([`0175c8a`](https://github.com/n24q02m/better-telegram-mcp/commit/0175c8a1526331d686598d8703b5010203dd9c20))

- Split telegram tool into message/chat/media/contact domains
  ([`4dc5022`](https://github.com/n24q02m/better-telegram-mcp/commit/4dc50227fcc89d8a810d8d5d6e0bf324ecfa0d3a))

### Refactoring

- Remove legacy auth flow, auto-open browser in relay setup
  ([`a2e27d1`](https://github.com/n24q02m/better-telegram-mcp/commit/a2e27d13c7ee588455aa9c91c7bfd78ae8d3b57b))

### Testing

- Add consolidated E2E test with relay/env/plugin and bot/user modes
  ([`6fcf715`](https://github.com/n24q02m/better-telegram-mcp/commit/6fcf715a6c99eb2d0dbebcbb41c1cf1dd67d7c4b))

### Breaking Changes

- Auth_server.py and auth_client.py are no longer used for user mode OTP authentication. All auth
  flows go through relay bidirectional messaging (mcp-relay-core).


## v3.5.0 (2026-03-31)

### Bug Fixes

- **cd**: Remove orphan build-auth-relay from sync-marketplace needs
  ([`1b588c4`](https://github.com/n24q02m/better-telegram-mcp/commit/1b588c415f5cf3936ea52a1f931c96e07f9a1f77))

- **deps**: Update non-major dependencies
  ([#92](https://github.com/n24q02m/better-telegram-mcp/pull/92),
  [`2996bb6`](https://github.com/n24q02m/better-telegram-mcp/commit/2996bb6fdb0883dcbf1a31bf1de7a48e57f4370d))

- **test**: Skip Unix-only path traversal tests on Windows
  ([#99](https://github.com/n24q02m/better-telegram-mcp/pull/99),
  [`e5a4c74`](https://github.com/n24q02m/better-telegram-mcp/commit/e5a4c7443001a686f6af1c472e49406f6d5a80b9))

### Chores

- **deps**: Lock file maintenance ([#93](https://github.com/n24q02m/better-telegram-mcp/pull/93),
  [`0a429c1`](https://github.com/n24q02m/better-telegram-mcp/commit/0a429c13ecb183c60fef681ba7c31abf90dbc63d))

### Continuous Integration

- Fix Qodo vertex_ai config, VERTEXAI_LOCATION, and Renovate PSR rule
  ([`72c7447`](https://github.com/n24q02m/better-telegram-mcp/commit/72c7447801634d8246eb84301d9d4b2c0971eaef))

- **cd**: Add plugin marketplace sync on stable release
  ([`4196543`](https://github.com/n24q02m/better-telegram-mcp/commit/4196543f52eb16586cd8ca551acef132a0ede390))

### Refactoring

- Remove orphan auth-relay, hardcode Telegram app credentials
  ([`83dde3b`](https://github.com/n24q02m/better-telegram-mcp/commit/83dde3b0e563e1342a2416b4f48d1cf0c7d9c34a))


## v3.5.0-beta.1 (2026-03-30)

### Bug Fixes

- Pin Docker base image SHA in auth-relay Dockerfile
  ([`1b74b88`](https://github.com/n24q02m/better-telegram-mcp/commit/1b74b88bd39d503239e349bbfb4d4254f3a0de6d))

- Resolve coverage regression and Windows test compatibility
  ([`0894b37`](https://github.com/n24q02m/better-telegram-mcp/commit/0894b37451ec68d4b080ad55e3a6d664057c4051))

### Features

- Add multi-user HTTP mode with per-user credential isolation
  ([#96](https://github.com/n24q02m/better-telegram-mcp/pull/96),
  [`075b5b0`](https://github.com/n24q02m/better-telegram-mcp/commit/075b5b08ade1e833ac514fe20e915b5204289b01))


## v3.4.0 (2026-03-28)

### Bug Fixes

- Bump mcp-relay-core to >=1.0.5
  ([`50c0f66`](https://github.com/n24q02m/better-telegram-mcp/commit/50c0f6663bbfab6c3dbbffb4405a3d696e70c744))

- Check saved session files after relay skip
  ([`6dc591b`](https://github.com/n24q02m/better-telegram-mcp/commit/6dc591b742189e94b27a6302c3c5430618471b3f))

- Credential resolution order -- relay only when no local credentials
  ([`bfc90c6`](https://github.com/n24q02m/better-telegram-mcp/commit/bfc90c6f58b42f8075147f21a6b3b06058d61341))

- Pin Docker base images to SHA digests
  ([`2cbd9ba`](https://github.com/n24q02m/better-telegram-mcp/commit/2cbd9ba4c43039d10022a304fc2a14e6875b861b))

- Pin pre-commit hooks to commit SHA
  ([`b3e2333`](https://github.com/n24q02m/better-telegram-mcp/commit/b3e23339e7417c1ef3455172fe0baa596fffc4be))

- Send complete message to relay page after config saved
  ([`bef96aa`](https://github.com/n24q02m/better-telegram-mcp/commit/bef96aa01ed89dbe5770a831c65da3b17bfb552d))

- Skip auth_client when relay already handled user-mode setup
  ([`d68f2a1`](https://github.com/n24q02m/better-telegram-mcp/commit/d68f2a19c931f2c3ce570dd3bd4c800543a54427))

- **cd**: Remove empty env blocks from OIDC migration
  ([`faaf477`](https://github.com/n24q02m/better-telegram-mcp/commit/faaf477fef0e0c26f42e3bf579a745bea78a97b5))

- **cd**: Replace GH_PAT with GitHub App installation token
  ([`835b7bb`](https://github.com/n24q02m/better-telegram-mcp/commit/835b7bbf7468c301d1ce19a91df3a6acc95ca225))

- **cd**: Use PyPI OIDC trusted publishing instead of PYPI_TOKEN
  ([`8b2af0c`](https://github.com/n24q02m/better-telegram-mcp/commit/8b2af0c19b8765481806135439a0b23be600a821))

- **ci**: Consolidate SMTP_USERNAME and NOTIFY_EMAIL into one secret
  ([`7148b24`](https://github.com/n24q02m/better-telegram-mcp/commit/7148b2442c6d2330d3c8cbcdc9a433abd4b0e0ab))

- **ci**: Consolidate SMTP_USERNAME+PASSWORD into SMTP_CREDENTIAL
  ([`39558b4`](https://github.com/n24q02m/better-telegram-mcp/commit/39558b4dad966a228265099f8ab6cdc76c828332))

- **ci**: Remove CODECOV_TOKEN, use tokenless upload
  ([`3ee4fbc`](https://github.com/n24q02m/better-telegram-mcp/commit/3ee4fbc96bb2dceee8d0ffa1ea2d25da6c72dd2f))

- **ci**: Use Vertex AI WIF instead of GEMINI_API_KEY for code review
  ([`6ad4732`](https://github.com/n24q02m/better-telegram-mcp/commit/6ad473266a2f39cb452f0a00c08a3f5f8d64882a))

- **deps**: Update non-major dependencies
  ([#85](https://github.com/n24q02m/better-telegram-mcp/pull/85),
  [`918bd38`](https://github.com/n24q02m/better-telegram-mcp/commit/918bd385559a91005ea9e8628b78dbc06c6b86e4))

- **deps**: Update non-major dependencies
  ([#82](https://github.com/n24q02m/better-telegram-mcp/pull/82),
  [`ddafab8`](https://github.com/n24q02m/better-telegram-mcp/commit/ddafab81e723519346e34004f532102e5594d833))

### Chores

- **deps**: Lock file maintenance
  ([`931551d`](https://github.com/n24q02m/better-telegram-mcp/commit/931551dddd89b725a0d347723edfc8ebf0f78519))

- **deps**: Update actions/create-github-app-token action to v3
  ([#88](https://github.com/n24q02m/better-telegram-mcp/pull/88),
  [`4a075bd`](https://github.com/n24q02m/better-telegram-mcp/commit/4a075bdf0b0f7bd8afa0857f530304a26337350c))

- **deps**: Update codecov/codecov-action action to v6
  ([#83](https://github.com/n24q02m/better-telegram-mcp/pull/83),
  [`f124484`](https://github.com/n24q02m/better-telegram-mcp/commit/f124484ab811a8d3339a7a9f0e50023a506ab5ca))

- **deps**: Update google-github-actions/auth action to v3
  ([#89](https://github.com/n24q02m/better-telegram-mcp/pull/89),
  [`c8b6191`](https://github.com/n24q02m/better-telegram-mcp/commit/c8b6191c02d1c1e6e97ec0bcad2ebe2e70e863e0))

### Features

- Integrate Telegram OTP/2FA auth into relay messaging
  ([`b75ba48`](https://github.com/n24q02m/better-telegram-mcp/commit/b75ba48f18dcb7cb71dc7dcc48752a2c4dae0cd5))

- Relay-first startup — always show relay URL
  ([`83b56ab`](https://github.com/n24q02m/better-telegram-mcp/commit/83b56abeeb7412cb32435d8a00d310747c19d4dc))

- Unblock async init flow by running webbrowser.open as background task
  ([#66](https://github.com/n24q02m/better-telegram-mcp/pull/66),
  [`6ed2ba7`](https://github.com/n24q02m/better-telegram-mcp/commit/6ed2ba7471a557dcbaba5c73ee75c47cdf2df685))

### Performance Improvements

- Run webbrowser.open in background task to avoid blocking initialization
  ([#66](https://github.com/n24q02m/better-telegram-mcp/pull/66),
  [`6ed2ba7`](https://github.com/n24q02m/better-telegram-mcp/commit/6ed2ba7471a557dcbaba5c73ee75c47cdf2df685))

### Testing

- Fix relay_setup tests and improve coverage
  ([`664d6de`](https://github.com/n24q02m/better-telegram-mcp/commit/664d6de371f28e19b3e581cd631a62e564098b5e))


## v3.3.0 (2026-03-26)

### Chores

- Add server.json to PSR version_variables, sync version
  ([`55f9828`](https://github.com/n24q02m/better-telegram-mcp/commit/55f98281c48df8319a3b3d8b63ac3d47c4a944df))

- Clean up plugin manifest for best practices
  ([`ec970b4`](https://github.com/n24q02m/better-telegram-mcp/commit/ec970b435bf65b56ea6c607c410c26688f6644f1))

### Documentation

- Fix marketplace references, improve Gemini CLI extension config
  ([`c3c6b26`](https://github.com/n24q02m/better-telegram-mcp/commit/c3c6b26a0e701765558a2d12be0f7ad5cdf7641e))

- Standardize README structure
  ([`1c7cdcf`](https://github.com/n24q02m/better-telegram-mcp/commit/1c7cdcf480b0279fb88a470a9048e7ce6972505b))


## v3.3.0-beta.1 (2026-03-25)

### Bug Fixes

- Align gemini-extension.json key with plugin.json
  ([`02c2579`](https://github.com/n24q02m/better-telegram-mcp/commit/02c2579b5c04e26a9bb398839c975828bfe1a414))

- Auto-sync plugin.json version via PSR
  ([`952b6ca`](https://github.com/n24q02m/better-telegram-mcp/commit/952b6ca67e2f4c9d34c124e7eb866529dfebcc80))

- Correct plugin install commands per official docs
  ([`322a9e0`](https://github.com/n24q02m/better-telegram-mcp/commit/322a9e01789b24557bf44668045329b120a69448))

- Handle empty string credentials + remove empty env vars from configs
  ([`fc713ac`](https://github.com/n24q02m/better-telegram-mcp/commit/fc713ace1ccf83be248d5525c0d8b66b3e7cd72a))

- Remove env from README MCP config examples
  ([`112fe1a`](https://github.com/n24q02m/better-telegram-mcp/commit/112fe1a0fec1b4e48c839f6be2942a528649840f))

- Remove env vars from plugin.json to prevent overwriting user config
  ([`47997da`](https://github.com/n24q02m/better-telegram-mcp/commit/47997dafea5cf4ece403e90cfbdebc83a5519b68))

- Remove pr-title-check job from CI
  ([`8c7d0cf`](https://github.com/n24q02m/better-telegram-mcp/commit/8c7d0cff0a6761b19905f1da96172437880ed14a))

- Switch mcp-relay-core from git dep to published PyPI package
  ([#77](https://github.com/n24q02m/better-telegram-mcp/pull/77),
  [`76b207f`](https://github.com/n24q02m/better-telegram-mcp/commit/76b207f0d4daa04db199994c907cd282bf2c834f))

- Sync plugin.json version and add skills/hooks references
  ([`8d54d4f`](https://github.com/n24q02m/better-telegram-mcp/commit/8d54d4fec376db09ff1d4c1cd4d9ba79b6ab3932))

- Unify Plugin install section with marketplace + individual options
  ([`d47409c`](https://github.com/n24q02m/better-telegram-mcp/commit/d47409c6a124a9d209f0a3169ccce89e7a783d48))

- Update ruff pre-commit hook to v0.15.7
  ([`e74a65c`](https://github.com/n24q02m/better-telegram-mcp/commit/e74a65c5406e0d7ed0199a7271657f63fc710501))

- Use version_variables for JSON files in PSR config
  ([`bdfd83e`](https://github.com/n24q02m/better-telegram-mcp/commit/bdfd83e066d5db669f735df53ff08adf19309aa7))

### Chores

- Add docker-compose overlay for HTTP mode deployment
  ([#77](https://github.com/n24q02m/better-telegram-mcp/pull/77),
  [`76b207f`](https://github.com/n24q02m/better-telegram-mcp/commit/76b207f0d4daa04db199994c907cd282bf2c834f))

### Documentation

- Add relay files to CLAUDE.md file structure
  ([`1d557a7`](https://github.com/n24q02m/better-telegram-mcp/commit/1d557a7e8a741d23d7fb325e2eb20aec51f20209))

- Add zero-config relay setup section to README
  ([`fefe28a`](https://github.com/n24q02m/better-telegram-mcp/commit/fefe28a83bf0953507826374f7e3d464e1d0d086))

### Features

- Add complete env vars and pipx mode to plugin config
  ([`20f9dd5`](https://github.com/n24q02m/better-telegram-mcp/commit/20f9dd5b07231316ad7d99817aa14841f0feae90))

- Add Gemini CLI extension config with PSR version sync
  ([`372c34b`](https://github.com/n24q02m/better-telegram-mcp/commit/372c34be9f0da3834807787c29cb390b074e01b0))

- Add HTTP transport mode with encrypted credential store
  ([#77](https://github.com/n24q02m/better-telegram-mcp/pull/77),
  [`76b207f`](https://github.com/n24q02m/better-telegram-mcp/commit/76b207f0d4daa04db199994c907cd282bf2c834f))

- Add zero-env-config relay setup via mcp-relay-core
  ([#77](https://github.com/n24q02m/better-telegram-mcp/pull/77),
  [`76b207f`](https://github.com/n24q02m/better-telegram-mcp/commit/76b207f0d4daa04db199994c907cd282bf2c834f))

- Multi-mode plugin config (stdio + docker + http)
  ([`65677c9`](https://github.com/n24q02m/better-telegram-mcp/commit/65677c9c5143ca49c0d693c2bf65976d34679ede))

- Standardize README with MCP Resources, Security, collapsible clients
  ([`571b230`](https://github.com/n24q02m/better-telegram-mcp/commit/571b23067be1e7a8248260f7cd8829073947828e))

- Zero-env-config relay setup + HTTP transport mode
  ([#77](https://github.com/n24q02m/better-telegram-mcp/pull/77),
  [`76b207f`](https://github.com/n24q02m/better-telegram-mcp/commit/76b207f0d4daa04db199994c907cd282bf2c834f))


## v3.2.0 (2026-03-24)

### Bug Fixes

- Add gitleaks secret detection to pre-commit hooks
  ([`180fbd5`](https://github.com/n24q02m/better-telegram-mcp/commit/180fbd54f219946de45c118b9df8cc372491f27f))

- Apply ruff formatting to pass CI lint check
  ([`437cf10`](https://github.com/n24q02m/better-telegram-mcp/commit/437cf108568b3d02917db1877a9e62ad30a4a56c))

### Testing

- Add full/real bot mode tests via MCP protocol
  ([`77277b2`](https://github.com/n24q02m/better-telegram-mcp/commit/77277b28adca75a7f5ce5ba0aa58eef9b3aecf70))


## v3.2.0-beta.1 (2026-03-23)

### Bug Fixes

- Allow help/config tools without credentials, add actionable setup hints
  ([`125f855`](https://github.com/n24q02m/better-telegram-mcp/commit/125f855de78ea08adf92818e2fe5b24dd737082b))

- Correct plugin packaging paths and marketplace schema
  ([`d9065e0`](https://github.com/n24q02m/better-telegram-mcp/commit/d9065e03c458787637c0787274f8fd8e52d1cf52))

- Correct setup-bot skill to use env var instead of runtime config for bot token
  ([`c97797b`](https://github.com/n24q02m/better-telegram-mcp/commit/c97797bbd4a88043f0d6cc462ee8ee263d7ce83a))

- Improve tool descriptions and corrective errors for LLM call pass rate
  ([`6f79799`](https://github.com/n24q02m/better-telegram-mcp/commit/6f79799f0b47e7b38c9b1b9346a977f3a7912cca))

- Standardize README structure with plugin-first Quick Start
  ([`722fc45`](https://github.com/n24q02m/better-telegram-mcp/commit/722fc45dc516173dfe20835a8550d90dc6056b6f))

- Sync plugin.json and server.json to v3.1.2
  ([`9a365b0`](https://github.com/n24q02m/better-telegram-mcp/commit/9a365b0b3b67e5773e58c7a4f694e9f5171d633c))

### Chores

- **deps**: Lock file maintenance ([#46](https://github.com/n24q02m/better-telegram-mcp/pull/46),
  [`1ae96c6`](https://github.com/n24q02m/better-telegram-mcp/commit/1ae96c6265a268352761acf59ec16d6869032644))

- **deps**: Update non-major dependencies
  ([#45](https://github.com/n24q02m/better-telegram-mcp/pull/45),
  [`f44696f`](https://github.com/n24q02m/better-telegram-mcp/commit/f44696fe27bc463fc564accdf1e706756f1acfa5))

- **deps**: Update qodo-ai/pr-agent digest to 42d55d4
  ([#50](https://github.com/n24q02m/better-telegram-mcp/pull/50),
  [`23d29a2`](https://github.com/n24q02m/better-telegram-mcp/commit/23d29a2f26f6c0f3f69b2e62dfb8816b9d364700))

### Documentation

- Add TELEGRAM_BOT_TOKEN env to plugin.json and setup guide
  ([`6090687`](https://github.com/n24q02m/better-telegram-mcp/commit/6090687b946789dc844eb5133d993b31421a4eca))

- Standardize README sections and sync Also by table
  ([`5ccee24`](https://github.com/n24q02m/better-telegram-mcp/commit/5ccee242737dc2b0c1f0ca90c20432551d8fb2fa))

### Features

- Add plugin packaging with skills, hooks, and marketplace metadata
  ([`26c7d1e`](https://github.com/n24q02m/better-telegram-mcp/commit/26c7d1e0818fae8712aced32e5717a8d24f58e2b))

- Async help tool I/O ([#52](https://github.com/n24q02m/better-telegram-mcp/pull/52),
  [`f26cd4b`](https://github.com/n24q02m/better-telegram-mcp/commit/f26cd4bbc7602fea23283bf37b50440da84f6585))

- Improve tool descriptions and error messages for better LLM pass rate
  ([`9b9909e`](https://github.com/n24q02m/better-telegram-mcp/commit/9b9909e74467cdd25238a72b39f0dd4aa231b3c6))

### Refactoring

- Redesign skills/hooks per approved spec
  ([`e933160`](https://github.com/n24q02m/better-telegram-mcp/commit/e93316006ff2e9b001f55179f8419b01197190d5))

### Testing

- Add pytest-based live MCP protocol tests
  ([`2013653`](https://github.com/n24q02m/better-telegram-mcp/commit/201365372f12ec0befb5bb4975d8bcf0e026eead))


## v3.1.2 (2026-03-20)

### Bug Fixes

- Improve auth web form UX
  ([`4f2db45`](https://github.com/n24q02m/better-telegram-mcp/commit/4f2db458f0af3382693d8c342f823dd775a86760))

- Rewrite README for accuracy and completeness
  ([`d3262e9`](https://github.com/n24q02m/better-telegram-mcp/commit/d3262e9a3880121ba9d9096fc991e6cc2da23af2))


## v3.1.1 (2026-03-20)

### Bug Fixes

- Add IPv4-mapped IPv6 to SSRF blocklist
  ([#44](https://github.com/n24q02m/better-telegram-mcp/pull/44),
  [`59aee2c`](https://github.com/n24q02m/better-telegram-mcp/commit/59aee2ce996925e312d351fa6c5270fedf511c54))

- Use Path.is_relative_to for path containment checks and expand tool reference docs
  ([`3445da7`](https://github.com/n24q02m/better-telegram-mcp/commit/3445da78345efb13269fda6e7d7a239c01af84ca))

- **ci**: Remove job-level continue-on-error from dependency-review
  ([`86aeea1`](https://github.com/n24q02m/better-telegram-mcp/commit/86aeea1016de4f84d88e3f99fbe35dc0f29807e8))

### Chores

- **deps**: Lock file maintenance ([#23](https://github.com/n24q02m/better-telegram-mcp/pull/23),
  [`1def987`](https://github.com/n24q02m/better-telegram-mcp/commit/1def9878cba893747f9fa23470031d332763d609))

- **deps**: Update codecov/codecov-action digest to 1af5884
  ([#27](https://github.com/n24q02m/better-telegram-mcp/pull/27),
  [`c094a15`](https://github.com/n24q02m/better-telegram-mcp/commit/c094a15bcb1750aff96090dd5498d792877ca678))

- **deps**: Update dawidd6/action-send-mail action to v16
  ([#26](https://github.com/n24q02m/better-telegram-mcp/pull/26),
  [`cc137f4`](https://github.com/n24q02m/better-telegram-mcp/commit/cc137f4cda77b031fb5d9753f4a1b8cc12658986))

### Documentation

- Add PRIVACY.md for data handling transparency
  ([`43cdd94`](https://github.com/n24q02m/better-telegram-mcp/commit/43cdd945cd649f82179795746760dd4552e5b6e4))

- Standardize README, SECURITY, CONTRIBUTING per cross-repo audit
  ([`ba851c7`](https://github.com/n24q02m/better-telegram-mcp/commit/ba851c7ae4646dd149f67a50a20f839a4c2db4c9))

### Performance Improvements

- Replace get_messages/get_dialogs with iter_messages/iter_dialogs
  ([#28](https://github.com/n24q02m/better-telegram-mcp/pull/28),
  [`bbcd88a`](https://github.com/n24q02m/better-telegram-mcp/commit/bbcd88a7b2531ec68918e7d4b6d776756eeee022))


## v3.1.0 (2026-03-18)

### Bug Fixes

- Remove auth secret, use token-based auth for public relay
  ([`df7d544`](https://github.com/n24q02m/better-telegram-mcp/commit/df7d54425691c9bf65fb0608a5e79bd5d1bbb9c2))

### Features

- Add auth-relay Docker build to CD pipeline
  ([`bc097f0`](https://github.com/n24q02m/better-telegram-mcp/commit/bc097f0e5d133eb805e8b74c979561f5f95f5d05))


## v3.0.0 (2026-03-18)

### Features

- Dual-mode auth (local + remote relay) with security hardening
  ([`5a7cece`](https://github.com/n24q02m/better-telegram-mcp/commit/5a7cecee89ca83f6c2723fba90c6097b7366d015))

### Breaking Changes

- Config tool `auth` and `send_code` actions removed. Authentication is now handled exclusively via
  web UI (local or remote).


## v2.0.0 (2026-03-17)

### Bug Fixes

- Remove terminal popup auth, simplify to CLI-first auth flow
  ([`dc9d5c6`](https://github.com/n24q02m/better-telegram-mcp/commit/dc9d5c6b261ba853e938c00edc58b1cd34e9dd5f))

### Features

- Add web-based OTP auth flow for MCP server
  ([`670ba67`](https://github.com/n24q02m/better-telegram-mcp/commit/670ba67d1d4fedd5b447193934a48a6397bfa2fd))

- Remove CLI auth, web UI is the only auth method
  ([`c0d02cf`](https://github.com/n24q02m/better-telegram-mcp/commit/c0d02cf63303ed53980dc20bde1a14057af9ba6a))

- Remove TELEGRAM_PASSWORD env var, 2FA via web UI only
  ([`caa3195`](https://github.com/n24q02m/better-telegram-mcp/commit/caa3195327a72aed7c4ada93c9d9e4a8491629aa))

### Breaking Changes

- `TELEGRAM_PASSWORD` env var no longer supported. 2FA passwords are now entered exclusively through
  the web auth UI or via curl POST /verify with {"code":"...", "password":"..."}.


## v1.3.0 (2026-03-17)

### Bug Fixes

- Add security hardening for path traversal, SSRF, and info disclosure
  ([`2f2e200`](https://github.com/n24q02m/better-telegram-mcp/commit/2f2e2009f64a93baf1bb1c4713f641a6f9cdefcf))

- Fix 'Too many arguments in chats' code health issue
  ([#5](https://github.com/n24q02m/better-telegram-mcp/pull/5),
  [`a872546`](https://github.com/n24q02m/better-telegram-mcp/commit/a87254680a7f4076de76ae4af98155b6bc1a3b89))

- Prevent command injection in terminal execution
  ([#12](https://github.com/n24q02m/better-telegram-mcp/pull/12),
  [`9655bb9`](https://github.com/n24q02m/better-telegram-mcp/commit/9655bb93d01dbfe84f07f841a3791c8e27810ab3))

- Resolve ty type checker CI failure and align README with portfolio standard
  ([`8906b49`](https://github.com/n24q02m/better-telegram-mcp/commit/8906b49de61af1f90be760aedfd85bd1a42cd9d1))

- **ci**: Use pull_request_target for jobs requiring secrets
  ([`16d9204`](https://github.com/n24q02m/better-telegram-mcp/commit/16d92044b7c5b96437822e1964ade8c381c0d95e))

- **deps**: Update non-major dependencies
  ([#18](https://github.com/n24q02m/better-telegram-mcp/pull/18),
  [`060b5ce`](https://github.com/n24q02m/better-telegram-mcp/commit/060b5ce218ae202ee723f4532265555d1bf3e3ce))

### Chores

- Standardize repo files across MCP server portfolio
  ([`5756415`](https://github.com/n24q02m/better-telegram-mcp/commit/57564158767a72ba10dffe04f66ba13a514098a0))

- Trigger Glama repo resync after history rewrite
  ([`3c69363`](https://github.com/n24q02m/better-telegram-mcp/commit/3c693632bb792177ab69e5ba27b29ed211964e72))

- **config**: Migrate config renovate.json
  ([#21](https://github.com/n24q02m/better-telegram-mcp/pull/21),
  [`35a12ab`](https://github.com/n24q02m/better-telegram-mcp/commit/35a12ab44a6b6da849858a867a7de86d5dcf6033))

- **deps**: Lock file maintenance ([#20](https://github.com/n24q02m/better-telegram-mcp/pull/20),
  [`09aaed9`](https://github.com/n24q02m/better-telegram-mcp/commit/09aaed91057a03689a86c23ec489c84339f8466d))

- **deps**: Update actions/download-artifact digest to 3e5f45b
  ([#15](https://github.com/n24q02m/better-telegram-mcp/pull/15),
  [`8d4cb4e`](https://github.com/n24q02m/better-telegram-mcp/commit/8d4cb4ed20238e23b27d69343cda0ead1ff03b1f))

- **deps**: Update astral-sh/setup-uv digest to 37802ad
  ([#16](https://github.com/n24q02m/better-telegram-mcp/pull/16),
  [`76c8e27`](https://github.com/n24q02m/better-telegram-mcp/commit/76c8e273cd74ab3c38056579202d4cf347afd9bb))

- **deps**: Update dawidd6/action-send-mail action to v15
  ([#19](https://github.com/n24q02m/better-telegram-mcp/pull/19),
  [`3acb374`](https://github.com/n24q02m/better-telegram-mcp/commit/3acb374ffc76720b83f56b1938c12114d0b10eea))

- **deps**: Update step-security/harden-runner digest to fa2e9d6
  ([#17](https://github.com/n24q02m/better-telegram-mcp/pull/17),
  [`3e7819a`](https://github.com/n24q02m/better-telegram-mcp/commit/3e7819a96cecd4645f3b4d34f41bd84bac5ab40c))

### Code Style

- Format test_user_backend.py with ruff
  ([#6](https://github.com/n24q02m/better-telegram-mcp/pull/6),
  [`2d10e35`](https://github.com/n24q02m/better-telegram-mcp/commit/2d10e3522af07ca8a6cf76bab2a3c0d91048abe2))

### Features

- Add test for clear_cache exception handling
  ([#6](https://github.com/n24q02m/better-telegram-mcp/pull/6),
  [`2d10e35`](https://github.com/n24q02m/better-telegram-mcp/commit/2d10e3522af07ca8a6cf76bab2a3c0d91048abe2))

- Refactor `messages` tool to use `MessagesArgs` struct model
  ([#10](https://github.com/n24q02m/better-telegram-mcp/pull/10),
  [`9fecb96`](https://github.com/n24q02m/better-telegram-mcp/commit/9fecb96b68235be04488249d7fafe13718ab5061))

- Refactor config tool to extract match cases into separate functions
  ([#7](https://github.com/n24q02m/better-telegram-mcp/pull/7),
  [`92f06c1`](https://github.com/n24q02m/better-telegram-mcp/commit/92f06c13038ab1fbc8b5ca562d87beda66be7cca))

- Test: cover send_code exception in user mode lifespan
  ([#4](https://github.com/n24q02m/better-telegram-mcp/pull/4),
  [`e7986b6`](https://github.com/n24q02m/better-telegram-mcp/commit/e7986b66839e0644d5d14a0e1a7e2355a028bce3))

### Testing

- Add clear_cache exception test ([#6](https://github.com/n24q02m/better-telegram-mcp/pull/6),
  [`2d10e35`](https://github.com/n24q02m/better-telegram-mcp/commit/2d10e3522af07ca8a6cf76bab2a3c0d91048abe2))

- Cover `send_code` exception in user mode lifespan
  ([#4](https://github.com/n24q02m/better-telegram-mcp/pull/4),
  [`e7986b6`](https://github.com/n24q02m/better-telegram-mcp/commit/e7986b66839e0644d5d14a0e1a7e2355a028bce3))

- Cover `send_code` exception in user mode lifespan and fix formatting
  ([#4](https://github.com/n24q02m/better-telegram-mcp/pull/4),
  [`e7986b6`](https://github.com/n24q02m/better-telegram-mcp/commit/e7986b66839e0644d5d14a0e1a7e2355a028bce3))


## v1.2.0 (2026-03-15)

### Bug Fixes

- Remove real phone number and API ID from README examples
  ([`bf55ea4`](https://github.com/n24q02m/better-telegram-mcp/commit/bf55ea40a5827e6e3147043a11c523b10c273af0))

### Chores

- Align repo structure, CI/CD, and config with reference MCP servers
  ([`30413ea`](https://github.com/n24q02m/better-telegram-mcp/commit/30413eafa864d8db02fbb1bfa33cf47e1375df9b))

### Documentation

- Rewrite README with runtime auth flow, fix user mode UX documentation
  ([`b80761d`](https://github.com/n24q02m/better-telegram-mcp/commit/b80761d6370b909f064c6f2820cc19fbccfa3558))

### Features

- Open terminal for direct OTP input, fallback to config tool for headless
  ([`56e7f08`](https://github.com/n24q02m/better-telegram-mcp/commit/56e7f08298f3babdf90bec213db8504b3957d8c1))


## v1.1.2 (2026-03-15)

### Bug Fixes

- List_contacts uses GetContactsRequest (get_contacts not in Telethon)
  ([`658e9a7`](https://github.com/n24q02m/better-telegram-mcp/commit/658e9a7e59030284ee1e29d22347b208b4997534))

### Testing

- Add user mode integration tests with live MTProto API
  ([`658e9a7`](https://github.com/n24q02m/better-telegram-mcp/commit/658e9a7e59030284ee1e29d22347b208b4997534))


## v1.1.1 (2026-03-15)

### Bug Fixes

- Catch send_code errors in lifespan to prevent server crash
  ([`79ac576`](https://github.com/n24q02m/better-telegram-mcp/commit/79ac5765c68a8b9fbd06074e2d9552aabf44667c))


## v1.1.0 (2026-03-15)

### Features

- Automatic runtime auth via config tool, remove mandatory auth CLI
  ([`f896f27`](https://github.com/n24q02m/better-telegram-mcp/commit/f896f27c1b54423da9477e7ef0124b64e9b92dc6))

### Testing

- Add bot mode integration tests with live Telegram API
  ([`eb6316b`](https://github.com/n24q02m/better-telegram-mcp/commit/eb6316b112d952af45c9d9b6717ea987aac902bb))


## v1.0.8 (2026-03-15)

### Bug Fixes

- Add email notify CI job, sync all GitHub secrets, fix minor issues
  ([`a6eca53`](https://github.com/n24q02m/better-telegram-mcp/commit/a6eca5306dbcee78c555b899024904cc8e432289))


## v1.0.7 (2026-03-15)

### Bug Fixes

- Add mcp-name to README for MCP Registry ownership verification
  ([`9b277d9`](https://github.com/n24q02m/better-telegram-mcp/commit/9b277d9d6da9503c28d30185e8941bbd4df6b2fa))


## v1.0.6 (2026-03-15)

### Bug Fixes

- Shorten server.json description to <= 100 chars for MCP Registry
  ([`fa1a39d`](https://github.com/n24q02m/better-telegram-mcp/commit/fa1a39dcba9062382782a29498b3e8440e1706ec))


## v1.0.5 (2026-03-15)

### Bug Fixes

- Add description and repository to server.json for MCP Registry
  ([`a921541`](https://github.com/n24q02m/better-telegram-mcp/commit/a921541aac8edf1fa292f125b2a27db835a38cd7))


## v1.0.4 (2026-03-15)

### Bug Fixes

- Remove LICENSE from .dockerignore, improve README with auth docs and troubleshooting
  ([`1d588c7`](https://github.com/n24q02m/better-telegram-mcp/commit/1d588c75c11d0e3bd3e2f528552deed53eecf506))


## v1.0.3 (2026-03-15)

### Bug Fixes

- Add ty rule ignores for Telethon dynamic types
  ([`925bffc`](https://github.com/n24q02m/better-telegram-mcp/commit/925bffc3233861355f6f58a58e9f65760c61749e))


## v1.0.2 (2026-03-15)

### Bug Fixes

- Implement config.set/cache_clear, topics.list, add missing repo files
  ([`bd385cb`](https://github.com/n24q02m/better-telegram-mcp/commit/bd385cb75c8a2ecb35d76fe3f71fae9e9dc95d76))


## v1.0.1 (2026-03-15)

### Bug Fixes

- Copy README.md and LICENSE in Dockerfile for uv build
  ([`2a907b4`](https://github.com/n24q02m/better-telegram-mcp/commit/2a907b4747bd9137a48a9afcaf069cda8799d012))


## v1.0.0 (2026-03-15)

- Initial Release
