# syntax=docker/dockerfile:1

FROM python:3.10-alpine as builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.10-alpine

WORKDIR /app

RUN apk add --no-cache postgresql-dev

COPY --from=builder /app/wheels /wheels
COPY . .

RUN pip install --no-cache /wheels/*
