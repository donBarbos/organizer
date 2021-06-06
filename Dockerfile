FROM python:3.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY app.py .
COPY organizer/ .
COPY locales/ .
COPY requirements.txt .

RUN apt update && apt upgrade && python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENV BOT_TOKEN=""
CMD ["python", "app.py"]
