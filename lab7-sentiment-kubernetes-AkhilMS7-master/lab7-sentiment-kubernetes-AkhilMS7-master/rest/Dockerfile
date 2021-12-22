FROM python:3.6-slim

WORKDIR /server

COPY rest-server.py /server/
COPY installations.txt /server/

RUN pip3 install -r installations.txt

ENTRYPOINT ["python", "rest-server.py"]