FROM python:buster

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

RUN apt update -y && apt install ffmpeg -y

RUN wget -O /usr/local/bin/yt-dlp https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp

COPY . .

RUN chmod +x run.sh

EXPOSE 443/tcp

ENTRYPOINT ["/bin/sh", "./run.sh"]
