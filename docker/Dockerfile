FROM python:3.11-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-cache

FROM python:3.11-slim
WORKDIR /app
RUN groupadd -r pythonuser && useradd -r -g pythonuser -m pythonuser

ENV UV_CACHE_DIR="/tmp/.uv_cache"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"
COPY . .

RUN chown -R pythonuser:pythonuser /app
USER pythonuser
CMD ["uv", "run","python", "src/main.py"]