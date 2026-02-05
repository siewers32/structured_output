FROM python:trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd -m appuser

WORKDIR /home/appuser/app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

# COPY ./src/requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

CMD [ "bash" ]