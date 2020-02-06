FROM ubuntu
RUN apt-get -y update && apt-get -y install \
    python3 \
    python3-pip
COPY ./alerting /tmp/alerting
RUN pip3 install -r /tmp/alerting/requirements.txt
CMD cd /tmp/alerting && python3 ./week-sslcert-notify.py
