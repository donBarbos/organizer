FROM python:3.9-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .

RUN apt update && \
    apt install --no-install-recommends -y build-essential curl && \
    #curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python && \
    pip install poetry && \
    poetry install --no-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["python", "-m", "organizer"]
