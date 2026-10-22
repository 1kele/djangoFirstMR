FROM ghcr.io/astral-sh/uv:0.13.1 AS uv_setup
FROM python:3.14-slim AS builder

COPY --from=uv_setup /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev


FROM python:3.14-slim AS runtime

RUN useradd -m appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY --chown=appuser:appuser . .

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/src

USER appuser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]