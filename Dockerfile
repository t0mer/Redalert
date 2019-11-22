FROM ubuntu:18.04

LABEL maintainer="tomer.klein@gmail.com"

#install pip3
RUN apt update

RUN apt install python3-pip wget --yes

#install python paho-mqtt client and urllib3
RUN pip3 install paho-mqtt urllib3

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

RUN mkdir /opt/redalert

RUN wget https://raw.githubusercontent.com/t0mer/Redalert/master/redalert.py -O /opt/redalert/redalert.py

ENTRYPOINT ["/usr/bin/python3", "/opt/redalert/redalert.py"]
