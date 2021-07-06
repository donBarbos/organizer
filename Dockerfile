FROM python:3.9-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD entrypoint.sh /entrypoint.sh

RUN apk update && \
    apk add --no-cache redis postgresql postgresql-contrib openrc && \
    rc-update add redis && \
    rc-update add postgresql && \
    apk add --no-cache python3-dev \
        musl-dev gcc postgresql-dev tzdata && \
    python -m pip install --upgrade pip && \
    pip install pipenv && \
    chmod +x /entrypoint.sh && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY . /usr/src/app

ENV BOT_TOKEN="110201544:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"
ENV PG_NAME="postgres"
ENV PG_USER="postgres"
ENV PG_PASSWORD=None
ENV PG_HOST=127.0.0.1
ENV PG_PORT=5432
ENV REDIS_HOST=127.0.0.1
ENV REDIS_PASSWORD=None
ENV REDIS_PORT=6379

ENTRYPOINT ["/entrypoint.sh"]
