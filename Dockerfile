FROM python:3.6

LABEL maintainer="tomer.klein@gmail.com"

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

COPY redalert.py /opt/redalert

ENTRYPOINT ["/usr/bin/python3", "/opt/redalert/redalert.py"]
