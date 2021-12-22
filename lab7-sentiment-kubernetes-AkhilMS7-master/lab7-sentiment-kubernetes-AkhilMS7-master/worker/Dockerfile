FROM dirkcgrunwald/flair

WORKDIR /server

COPY worker-server.py /server/
COPY installations.txt /server/

RUN pip3 install -r installations.txt

ENTRYPOINT ["python", "worker-server.py"]