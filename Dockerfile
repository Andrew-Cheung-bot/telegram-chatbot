FROM python:3.9.19-slim-bullseye

WORKDIR /APP
COPY . /APP

RUN pip install update
RUN pip install -r requirements.txt

CMD python chatbot.py