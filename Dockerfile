FROM continuumio/miniconda3:4.7.12

RUN mkdir /app
WORKDIR /app

RUN apt-get -y update
RUN apt-get -y install build-essential libcairo2 libpango-1.0-0 \
 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

ADD requirements.txt .
ADD src .
ADD documents .

RUN pip install -r requirements.txt