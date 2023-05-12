FROM python:3.10-alpine

COPY Requirements.txt .

RUN pip install --no-cache-dir -r Requirements.txt

COPY . .

RUN chmod +x run.sh

ENTRYPOINT [ "/bin/sh","./run.sh" ]