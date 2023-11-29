# Base image
FROM python:3.9

ENV MICRO_SERVICE=/home/app/api_nlp

RUN mkdir -p $MICRO_SERVICE
RUN mkdir -p $MICRO_SERVICE/static

# where the code lives
WORKDIR $MICRO_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get -y update
RUN apt-get -y upgrade
RUN pip install --upgrade pip

# copy all project
COPY . $MICRO_SERVICE


#install project requirements
RUN pip install -r requirements.txt

# where the code lives
WORKDIR $MICRO_SERVICE

# expose the port that Flask will run on
EXPOSE 5000

# run entry point
CMD ["python", "runserver.py"]


