FROM python:3.8

RUN apt-get update

ADD ./requirements.txt /config/requirements.txt
RUN pip install -r /config/requirements.txt

ADD search_engine /app/search_engine
ADD parlai /app/parlai
RUN pip install -e /app/parlai
