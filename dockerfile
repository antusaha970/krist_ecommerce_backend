FROM python:3.11.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache bash

WORKDIR /krist_ecommerce_backend
COPY requirements.txt /krist_ecommerce_backend/
RUN pip install -r requirements.txt
COPY . /krist_ecommerce_backend/