FROM python:3-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN apt-get update &&\
 apt-get install -y libpq-dev gcc

RUN pip install -r requirements.txt

COPY . /code/

RUN apt-get autoremove -y gcc

CMD ["python","manage.py","runserver","0.0.0.0:8000"]