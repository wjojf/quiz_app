FROM python:3.11-alpine

ENV PATH="scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./app /app

WORKDIR /app

RUN touch core/management/commands/createa_admin.py
RUN touch core/management/commands/create_quiz.py