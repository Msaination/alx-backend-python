# Dockerfile
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     default-libmysqlclient-dev gcc && \
#     rm -rf /var/lib/apt/lists/*

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy project files
COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# FROM python:3.10-slim  
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1
# WORKDIR /app
# RUN pip install --upgrade pip
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt