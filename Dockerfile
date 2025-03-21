FROM python:3.8-slim

WORKDIR /usr/src/app

COPY ./aws-batch/ .

CMD ["python", "./app.py"]
