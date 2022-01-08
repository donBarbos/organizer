<h1 align="center"><em>Telegram bot for reminders.</em></h1>

<p align="center">
<a href="https://github.com/DONSIMON92/organizer/actions/workflows/checks.yml"><img src="https://github.com/DONSIMON92/organizer/actions/workflows/checks.yml/badge.svg" alt="Testing Status"></a>
<a href="https://www.python.org/downloads"><img src="https://img.shields.io/badge/Python-3.7%2B-blue" alt="Python"></a>
<a href="https://github.com/DONSIMON92/organizer/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style"></a>
<p>

<p align="center">a working example of this bot: https://t.me/Multitask_4Bot<p>

# Installation

## Running on Local Machine

- install dependencies using [Poetry](https://python-poetry.org "python package manager")
    ```
    poetry install
    ```
- configure environment variables in `.env` file

- start bot in virtual environment
    ```
    poetry run python -m organizer
    ```

## Launch in Docker

- configure environment variables in `.env` file

- start virtual environment
    ```
    poetry shell
    ```

- building the docker image
    ```
    docker-compose build
    ```
- start service
    ```
    docker-compose up -d
    ```

# Environment variables

- `BOT_TOKEN` — Telegram bot token
- `PG_HOST` — hostname or an IP address PostgreSQL database
- `PG_NAME` — the name of the PostgreSQL database
- `PG_PASSWORD` — password used to authenticate
- `PG_PORT` — connection port number (defaults to 5432 if not provided)
- `PG_USER` — the username used to authenticate
- `REDIS_HOST` — hostname or an IP address Redis database 
- `REDIS_PASSWORD` — Redis database password, empty by default
- `REDIS_PORT` — port from Redis database

> *I use Redis for Finite State Machine, and PostgreSQL as Database for storing notes*

# Tech Stack

- `aiogram` — asynchronous framework for Telegram Bot API
- `asyncpg` — asynchronous PostgreSQL database client library
- `poetry` — development workflow
- `loguru` — third party library for logging in Python
- `docker` — to automate deployment
- `postgres` — powerful, open source object-relational database system
- `redis` — an in-memory data structure store
