FROM python:3.10-alpine
ADD . /reclutamiento
WORKDIR /reclutamiento
RUN apk add --no-cache gcc musl-dev postgresql-dev
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]