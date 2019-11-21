FROM ubuntu:18.04

LABEL maintainer="tomer.klein@gmail.com"

#install pip3
RUN apt update && apt upgrade --yes

RUN install python3-pip

#install python paho-mqtt client and urllib3
pip3 install paho-mqtt urllib3

#Mqtt broker address (ip or fqdn)
ENV MQTT_HOST

#Mqtt broker port - 1883 is the common
ENV MQTT_PORT=1883

#Mqtt broker username
ENV MQTT_USER

#Mqtt broker password
ENV MQTT_PASS
