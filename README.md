# [Telegram bot](https://t.me/Multitask_4Bot "https://t.me/Multitask_4Bot") for reminders

[![Testing Status](https://github.com/DONSIMON92/organizer/actions/workflows/checks.yml/badge.svg)](https://github.com/DONSIMON92/organizer/actions/workflows/checks.yml)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/DONSIMON92/organizer/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> *you must provide yourself with a bot id in advance. you can register your bot with [BotFather](https://t.me/BotFather "https://t.me/BotFather")*

# Installation

## Running on Local Machine

- download code from github
    ```
    git clone git@github.com:DONSIMON92/organizer-bot.git
    ```
- install python package manager [Poetry](https://python-poetry.org) and install dependencies
    ```
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    poetry install
    ```
- configure environment variables in `.env` file

- start bot in virtual environment
    ```
    poetry run python -m organizer
    ```

## Launch in Docker

- download code from github
    ```
    git clone git@github.com:DONSIMON92/organizer-bot.git
    ```
- configure environment variables in `.env` file

- building the docker image
    ```
    docker-compose build
    ```
- start service
    ```
    docker-compose up
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
- `poetry` - development workflow
- `loguru` — third party library for logging in Python
- `docker` — to automate deployment
- `postgres` — powerful, open source object-relational database system
- `redis` — an in-memory data structure store
