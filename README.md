# [Telegram-bot](https://t.me/Multitask_4Bot "https://t.me/Multitask_4Bot") for reminders

> *you must provide yourself with a bot id in advance. you can register your bot with [BotFather](https://t.me/BotFather "https://t.me/BotFather")*

## How to run a bot on a server
- download code from github
    ```
    git clone git@github.com:DONSIMON92/organizer-bot.git
    ```
- create a virtual environment and activate it
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```
- import modules from requirements.txt
    ```
    pip3 install -r requirements.txt
    ```
- to connect your bot's token (put your token that [BotFather](https://t.me/BotFather "https://t.me/BotFather") issued instead of ellipsis)
    ```
    echo "BOT_TOKEN = '...'" > .env
    ```
- start bot
    ```
    python3 main.py
    ```
