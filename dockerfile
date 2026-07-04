FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev
COPY src/ src/
COPY main.py .
ENV PATH="/app/.venv/bin:$PATH"
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENTRYPOINT ["python", "main.py"]
