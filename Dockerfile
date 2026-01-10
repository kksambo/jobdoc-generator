# Use official Python image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for WeasyPrint and PDFs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpango1.0-dev \
    libgdk-pixbuf-xlib-2.0-0 \
    libgobject-2.0-0 \
    libxml2 \
    libxml2-dev \
    libxslt1-dev \
    wget \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Run Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
