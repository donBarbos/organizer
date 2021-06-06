# [Telegram-bot](https://t.me/Multitask_4Bot "https://t.me/Multitask_4Bot") for reminders

[![Build Status](https://github.com/DONSIMON92/organizer/actions/workflows/checks.yml/badge.svg)](https://github.com/DONSIMON92/organizer/actions/workflows/checks.yml) [![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/DONSIMON92/organizer/blob/master/LICENSE)

> *you must provide yourself with a bot id in advance. you can register your bot with [BotFather](https://t.me/BotFather "https://t.me/BotFather")*

# Installation

## Running on Local Machine

- download code from github
    ```
    git clone git@github.com:DONSIMON92/organizer-bot.git
    ```
- create a virtual environment and activate it
    ```
    python3 -m venv .venv \
    source .venv/bin/activate
    ```
- upgrade pip and import modules from requirements.txt
    ```
    python3 -m pip install --upgrade pip \
    pip3 install -r requirements.txt
    ```
- to connect your bot's token (put your token that [BotFather](https://t.me/BotFather "https://t.me/BotFather") issued instead of ellipsis)
    ```
    echo "BOT_TOKEN='...'" > .env
    ```
- start bot
    ```
    python3 app.py
    ```

## Start in Docker

- download code from github
    ```
    git clone git@github.com:DONSIMON92/organizer-bot.git
    ```
- put your telegram API into BOT_TOKEN variable in Dockerfile

- building the docker image
    ```
    docker build -t organizer-bot .
    ```
- start bot
    ```
    docker run --name organizer -d organizer-bot
    ```
