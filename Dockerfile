FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN [ "python3", "-c", "import nltk; nltk.download('all')" ]

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
