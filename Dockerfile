FROM python:3.11-slim

# lxml wheels cover linux/amd64+arm64, so no build toolchain needed.
WORKDIR /app

# Install dependencies first so source edits don't bust the layer cache.
COPY pyproject.toml README.md LICENSE ./
COPY craigsail/ craigsail/
RUN pip install --no-cache-dir .

COPY web_app/ web_app/

# The sqlite db and csv snapshots live here; compose mounts it as a volume.
RUN mkdir -p /app/data
ENV CRAIGSAIL_DB=/app/data/craigsail.db

EXPOSE 5000

CMD ["flask", "--app", "web_app.app", "run", "--host", "0.0.0.0"]
