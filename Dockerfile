FROM python:buster

WORKDIR /app

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

RUN apt update -y && apt install ffmpeg -y

COPY . .

RUN chmod +x run.sh

ENTRYPOINT ["/bin/sh", "./run.sh"]
