FROM python:3.11-slim-bullseye

WORKDIR /usr/src/app
COPY /app .

RUN apt-get update -y && \
    apt-get upgrade -y && \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000
CMD ["gunicorn", "--config", "gunicorn.conf.py", "main:app"]
