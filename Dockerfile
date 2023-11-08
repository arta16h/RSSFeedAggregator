FROM python:3.11

LABEL version="1.0.0"

LABEL maintainer="sevda.hayati2015@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /dockerrss

COPY requirements.txt .

RUN pip install -U pip

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    python manage.py runserver 0.0.0.0:8000