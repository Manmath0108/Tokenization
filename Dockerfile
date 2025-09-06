# Dockerfile - production-ready minimal image for FastAPI app

# 1) Base image: small, stable Python
FROM python:3.10-slim

# 2) Environment variables for predictable behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3) Create and set working directory
WORKDIR /app

# 4) Install system deps (if needed) and pip requirements.
#    We install build-essential only if required by some pip packages (kept minimal).
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# 5) Copy requirements first (leverages Docker cache)
COPY requirements.txt .

# 6) Install python dependencies with no cache
RUN pip install --no-cache-dir -r requirements.txt

# 7) Copy the rest of the app code
COPY . .

# 8) Expose port the app will run on
EXPOSE 8000

# 9) Default command to run the app with Uvicorn (production-friendly)
CMD ["uvicorn", "APIs.tokenizer_api:app", "--host", "0.0.0.0", "--port", "8000"]
