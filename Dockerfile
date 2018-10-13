FROM ubuntu:16.04

MAINTAINER Youssef El Khalili "elkhalili.youssef@outlook.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /qlik/requirements.txt

WORKDIR /qlik

RUN pip install -r requirements.txt

COPY . /qlik

EXPOSE 5000

CMD ["python", "run.py"]
