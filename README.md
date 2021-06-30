# [Telegram bot](https://t.me/Multitask_4Bot "https://t.me/Multitask_4Bot") for reminders

[![Testing Status](https://github.com/DONSIMON92/organizer/actions/workflows/checks.yml/badge.svg)](https://github.com/DONSIMON92/organizer/actions/workflows/checks.yml) [![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/DONSIMON92/organizer/blob/master/LICENSE)

> *you must provide yourself with a bot id in advance. you can register your bot with [BotFather](https://t.me/BotFather "https://t.me/BotFather")*

# Installation

## Running on Local Machine

- download code from github
    ```
    git clone git@github.com:DONSIMON92/organizer-bot.git
    ```
- configure a virtual environment
    ```
    pip3 install pipenv \
    pipenv sync
    ```
- configure environment variables in `.env` file

- start bot in virtual environment
    ```
    pipenv run python3 -m organizer
    ```

## Launch in Docker

- download code from github
    ```
    git clone git@github.com:DONSIMON92/organizer-bot.git
    ```
- configure environment variables in Dockerfile

- building the docker image
    ```
    docker build -t organizer-bot .
    ```
- start bot
    ```
    docker run --name organizer -d organizer-bot
    ```

# Environment variables

- `BOT_TOKEN` — Telegram bot token
- `PG_NAME` — the name of the PostgreSQL database
- `PG_USER` — the username used to authenticate
- `PG_PASSWORD` — password used to authenticate
- `PG_HOST` — host name or an IP address PostgreSQL database
- `PG_PORT` — connection port number (defaults to 5432 if not provided)
- `REDIS_HOST` - host name or an IP address Redis database 
- `REDIS_PASSWORD` - Redis database password, empty by default
- `REDIS_PORT` - port from Redis database

> *I use Redis for Finite State Machine, and PostgreSQL as Database for storing notes*

# Tech Stack

- `aiogram` — asynchronous framework for Telegram Bot API
- `asyncpg` — asynchronous PostgreSQL database client library
- `pipenv` - development workflow
- `loguru` — third party library for logging in Python
- `docker` — to automate deployment
- `postgres` — powerful, open source object-relational database system
- `redis` — an in-memory data structure store
