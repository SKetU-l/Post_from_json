FROM python:buster

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app/

COPY . .

EXPOSE 8080 443

RUN apt update -y && apt upgrade -y \
         apt install ffmpeg -y && \
         pip install --no-cache-dir -r req.txt && \
         wget -O /usr/local/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp && \
         chmod a+rx /usr/local/bin/yt-dlp && \
         chmod +x run.sh

ENTRYPOINT ["/bin/sh", "./run.sh"]
