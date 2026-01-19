# --- Stage 1: Builder ---
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Stage 2: Runtime ---
FROM python:3.11-slim

WORKDIR /app

# 1. Install System Dependencies (Cron, Timezone, and dos2unix)
RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# 2. Set Timezone to UTC
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 3. Copy Python Dependencies
COPY --from=builder /install /usr/local

# 4. Copy Application Code
COPY . .

# 5. Setup Cron Job
RUN mkdir -p /data /cron && \
    chmod 755 /data /cron

COPY cron/2fa-cron /etc/cron.d/2fa-cron

# FIX: Convert line endings from Windows (CRLF) to Linux (LF)
RUN dos2unix /etc/cron.d/2fa-cron

# Give execution rights
RUN chmod 0644 /etc/cron.d/2fa-cron

# Apply cron job
RUN crontab /etc/cron.d/2fa-cron

# 6. Expose API Port
EXPOSE 8080

# 7. Start Command
CMD cron && python -m uvicorn main:app --host 0.0.0.0 --port 8080