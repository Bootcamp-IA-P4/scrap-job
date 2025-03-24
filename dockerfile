# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files and keeps Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (required for Firefox, GeckoDriver, and Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    firefox-esr \
    libx11-xcb1 \
    libxss1 \
    libnss3 \
    libatk-bridge2.0-0 \
    libxtst6 \
    libxrender1 \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    libgl1-mesa-dri \
    libpci3 \
    xvfb \
    postgresql \
    postgresql-client \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy the requirements file into the container
COPY pyproject.toml poetry.lock ./

# Install project dependencies using Poetry
RUN poetry install --no-root

# Configure Fontconfig to avoid cache errors
RUN mkdir -p /tmp/cache/fontconfig && chmod 777 /tmp/cache/fontconfig
ENV FONTCONFIG_PATH=/tmp/cache/fontconfig

# Download and install GeckoDriver
RUN case $(dpkg --print-architecture) in \
    amd64) ARCH=linux64 ;; \
    arm64) ARCH=linux-aarch64 ;; \
    *) echo "Unsupported architecture" && exit 1 ;; \
    esac && \
    wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-$ARCH.tar.gz && \
    tar -xvzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# Copy the rest of the application code into the container
COPY . .

# Set up a virtual display for headless Firefox
ENV DISPLAY=:99

# Give run permissions to the entry_point script
RUN chmod +x /app/entry_point.sh

# Command to run the entrypoint script
ENTRYPOINT ["/app/entry_point.sh"]