FROM python:3.11-slim AS build

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    python3-distutils \
    libatlas-base-dev \
    liblapack-dev \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port on which the application will run
EXPOSE 8501

# Set environment variables for Python (optional but recommended)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "streamlit", "service/lab_app.py"]