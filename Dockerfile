FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv python3-dev git

COPY . /opt/netztp

ENV VIRTUALENV /opt/netztp/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH $VIRTUALENV/bin:$PATH

RUN pip install -r /opt/netztp/requirements.txt

EXPOSE 8001/tcp

ENTRYPOINT ["gunicorn", "--pythonpath", "/opt/netztp", "--config", "/opt/netztp/gunicorn.py", "wsgi:app"]
