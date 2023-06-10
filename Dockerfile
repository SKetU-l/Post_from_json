FROM python:3.10-alpine

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

RUN apk add --no-cache ffmpeg

RUN wget -O /usr/local/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp

COPY . .

RUN chmod +x run.sh

ENTRYPOINT ["/bin/sh", "./run.sh"]
