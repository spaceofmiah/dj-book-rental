FROM python:3.11-alpine


WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && apk upgrade && apk add poetry  

COPY pyproject.toml .
RUN poetry install --no-root

COPY . /app/

COPY ./scripts/run.sh /app/
RUN chmod +x /app/scripts/run.sh
RUN chmod 777 /app/scripts/run.sh
RUN mv /app/scripts/run.sh /app/run.sh
