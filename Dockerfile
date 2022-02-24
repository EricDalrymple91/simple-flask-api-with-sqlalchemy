FROM python:3.9

RUN apt-get update && apt-get install -y bash

# install Flask
ADD . /
RUN python -m venv venv2

RUN pip install -r requirements.txt

# copy our minimal Gunicorn example
COPY app/ /

ENTRYPOINT [ "gunicorn", "app:app", "-w", "4", "-b", ":8080", "--timeout", "120" ]