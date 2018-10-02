FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
RUN mkdir /src
RUN mkdir /static
WORKDIR /src
ADD ./src /src
RUN pip install -r requirements.pip
CMD python manage.py collectstatic --no-input;python manage.py migrate; gunicorn mydjango.wsgi --reload -b 0.0.0.0:8000
ADD . /code/
