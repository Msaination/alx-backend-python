# Dockerfile
# ✅ Base image
FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

# ✅ Set work directory inside container
WORKDIR /app
# ✅ Upgrade pip
RUN pip install --upgrade pip   

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ✅ Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy project code
COPY . /app/

# ✅ Expose Django default port
EXPOSE 8000
# -p 8000

# ✅ Run server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
