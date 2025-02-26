FROM python:3.11-slim AS build

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    python3-dev \
    python3-distutils \
    libatlas-base-dev \
    liblapack-dev \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Example: install ollama CLI if available for Linux
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy the rest of the application code to the container
COPY . /app/

# Expose the port on which the application will run
EXPOSE 8501

# Set environment variables for Python (optional but recommended)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the app
CMD ["sh", "-c", "ollama serve & streamlit run app/lab_app.py"]