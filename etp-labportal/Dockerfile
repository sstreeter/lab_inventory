# Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Copy .env first (for caching benefits), then the rest
COPY . .

# Optional: Set which env file to load
ENV ENV_FILE=.env.dev       # Uncomment for development
# ENV ENV_FILE=.env.test    # Uncomment for testing
# ENV ENV_FILE=.env.prod    # Uncomment for production

# Install python-dotenv if not already listed
# (Add it to requirements.txt too)
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Default: use flask for dev
CMD ["flask", "run", "--port=8000"]
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app"]
