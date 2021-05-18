# [Telegram-bot](https://t.me/Multitask_4Bot "https://t.me/Multitask_4Bot") for reminders

> *you must provide yourself with a bot id in advance. you can register your bot with [BotFather](https://t.me/BotFather "https://t.me/BotFather")*

## How to run a bot on a server
- download code from github
    ```
    git clone https://github.com/DONSIMON92/organizer-bot.git
    ```
    or (if you have official github CLI)
    ```
    gh repo clone DONSIMON92/organizer-bot
    ```
- create a virtual environment and activate it
    ```
    python3 -m venv .env
    source .env/bin/activate
    ```
- import modules from requirements.txt
    ```
    pip3 install -r requirements.txt
    ```
- to connect your bot's token (put your token that [BotFather](https://t.me/BotFather "https://t.me/BotFather") issued instead of ellipsis)
    ```
    echo "BOT_TOKEN = '...'" >> config.py
    ```
- start bot
    ```
    python3 main.py
    ```
