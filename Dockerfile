# syntax=docker/dockerfile:1
# Multi-stage build for telegram (Telegram MCP server)
# Python 3.13 + httpx (Bot API) + Telethon (MTProto)

# ========================
# Stage 1: Builder
# ========================
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim@sha256:531f855bda2c73cd6ef67d56b733b357cea384185b3022bd09f05e002cd144ca AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# git is needed by uv to fetch the n24q02m-hull git pin (pyproject.toml) until
# hull is on PyPI; builder stage only, the runtime image copies the venv.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first (cached when deps don't change)
# Strip [tool.uv.sources] local path overrides so uv resolves from PyPI
COPY pyproject.toml uv.lock ./
RUN sed -i '/^\[tool\.uv\.sources\]/,/^$/d' pyproject.toml && cp uv.lock /tmp/uv.lock.docker
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy application code and install the project
COPY . /app
RUN sed -i '/^\[tool\.uv\.sources\]/,/^$/d' pyproject.toml && cp /tmp/uv.lock.docker uv.lock
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ========================
# Stage 2: Runtime base (shared by stdio + http targets)
# ========================
# Multi-target Dockerfile.
# Build stdio: `docker buildx build --target stdio -t <repo>:stdio .`
# Build http:  `docker buildx build --target http  -t <repo>:http .`
# Build latest (= http): `docker buildx build --target http -t <repo>:latest .`
FROM python:3.13-slim-bookworm@sha256:ed86c82274b3c69b52fb5820f358f0bd7df0b603332063cb5c6e32bd220c3e6e AS runtime

LABEL org.opencontainers.image.source="https://github.com/n24q02m/telegram"
LABEL io.modelcontextprotocol.server.name="io.github.n24q02m/better-telegram-mcp"

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1 \
    TELEGRAM_DATA_DIR=/data

# Create non-root user and set permissions
RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser -m appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /app /data /home/appuser

VOLUME /data
USER appuser

# ========================
# Stage 3a: stdio target (default for plugin marketplace & uvx-style usage)
# ========================
FROM runtime AS stdio
ENV MCP_TRANSPORT=stdio
ENTRYPOINT ["python", "-m", "telegram"]

# ========================
# Stage 3b: http target (self-hosted daemon)
# ========================
# hull reads server settings from ~/.telegram/config.toml, so the bind address
# is passed on the command line. Mount /home/appuser/.telegram/config.toml with
# auth = "token" or "multi": "no-auth" refuses a non-loopback bind (exit 2).
FROM runtime AS http
ENV MCP_TRANSPORT=http
EXPOSE 8080
ENTRYPOINT ["python", "-m", "telegram", "--http", "--host", "0.0.0.0", "--port", "8080"]
