FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src

# Install system dependencies
RUN apt-get update && apt-get install -y gcc

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Set env vars (optional)
ENV PYTHONUNBUFFERED=1

# Expose FastAPI port
EXPOSE 3000

# Run FastAPI app using Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"]
