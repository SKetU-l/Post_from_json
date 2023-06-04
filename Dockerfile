FROM python:3.10-alpine

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run.sh

ENTRYPOINT [ "/bin/sh","./run.sh" ]
