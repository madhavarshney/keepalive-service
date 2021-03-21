FROM python:3.8-slim

WORKDIR /keepalive-service

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN touch config.yaml

CMD [ "python3", "-m" , "keepalive" ]
