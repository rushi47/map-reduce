FROM alpine

FROM python

RUN mkdir /app

ADD mapper.py master.py requirement.txt /app

RUN  pip install -r /app/requirement.txt

ENTRYPOINT python /app/mapper.py