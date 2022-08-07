FROM ubuntu:18.04

LABEL maintainer="tomer.klein@gmail.com"

#install pip3
RUN apt update

RUN apt install -yqq python3-pip

#install python paho-mqtt client and urllib3
RUN pip3 install --upgrade pip setuptools  --no-cache-dir && \
    pip3 install paho-mqtt --no-cache-dir && \
    pip3 install urllib3 --no-cache-dir && \
    pip3 install loguru --no-cache-dir && \
    pip3 install apprise --no-cache-dir


ENV PYTHONIOENCODING=utf-8

ENV LANG=C.UTF-8

#Mqtt broker address (ip or fqdn)
ENV MQTT_HOST "127.0.0.1"

#Mqtt broker port - 1883 is the common
ENV MQTT_PORT "1883"

#Mqtt broker username
ENV MQTT_USER "user"

#Mqtt broker password
ENV MQTT_PASS "password"

#Debug Mode for testing
ENV DEBUG_MODE "False"

ENV REGION "*"

ENV NOTIFIERS ""

ENV INCLUDE_TEST_ALERTS = "False"

#Create working directory
RUN mkdir /opt/redalert

COPY redalert.py /opt/redalert

#Cleanup
#RUN apt remove python3-pip --yes && \
#    apt autoremove --yes && \
#    rm -rf /var/cache/*


ENTRYPOINT ["/usr/bin/python3", "/opt/redalert/redalert.py"]
