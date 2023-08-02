FROM python:buster

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app/

COPY . .

EXPOSE 8080 443

RUN apt update -y && apt upgrade -y \
    apt install ffmpeg -y && \
    pip install --no-cache-dir -r req.txt && \
    chmod +x run.sh

ENTRYPOINT ["/bin/sh", "./run.sh"]
