# FROM python:3.11-slim
# ENV PYTHONDONTWRITEBYTECODE=1 \ 
# PYTHONBUFFERED=1
# WORKDIR /app
# RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/list/*
# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# COPY . . /app/
# EXPOSE 8000
# CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", "0.0.0.0:8000"]
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
# CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", "0.0.0.0:8000 "]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]




