FROM alpine

FROM python

RUN apt-get update && apt-get install -y vim

RUN mkdir /app

ADD app /app/

ADD page_rank_data /app/page_rank_data

RUN  pip install -r /app/requirement.txt

ENTRYPOINT python /app/reducer_pr.py