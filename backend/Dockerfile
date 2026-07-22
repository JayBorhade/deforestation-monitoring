FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    gdal-bin \
    libgdal-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements first for layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy app
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
