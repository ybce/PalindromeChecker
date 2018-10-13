FROM ubuntu:16.04

MAINTAINER Youssef El Khalili "elkhalili.youssef@outlook.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "qlik.py"]
