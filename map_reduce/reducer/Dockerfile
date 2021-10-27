FROM alpine

FROM python

RUN apt-get update && apt-get install -y vim

RUN mkdir /app

ADD app /app/

RUN  pip install -r /app/requirement.txt

ENTRYPOINT python /app/reducer.py