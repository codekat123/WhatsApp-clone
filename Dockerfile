FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


COPY . /app/

ENV DJANGO_SETTINGS_MODULE=src.settings

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "src.asgi:application"]
