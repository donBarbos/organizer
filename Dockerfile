FROM python:3.9-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .

RUN apt update && \
    apt install --no-install-recommends -y build-essential curl && \
    /usr/local/bin/python -m pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["python", "-m", "organizer"]
