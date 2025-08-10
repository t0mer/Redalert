FROM ubuntu:20.04

LABEL maintainer="tomer.klein@gmail.com"

#install pip3
RUN apt update && \
    apt install -yqq python3-pip && \
    apt clean



#install python paho-mqtt client and urllib3
RUN pip3 install --upgrade pip setuptools  --no-cache-dir && \
    pip3 install paho-mqtt==1.6.1 --no-cache-dir && \
    pip3 install urllib3 --no-cache-dir && \
    pip3 install loguru --no-cache-dir && \
    pip3 install requests --no-cache-dir && \
    pip3 install apprise --no-cache-dir && \
    pip3 install websocket-client --no-cache-dir && \
    pip3 install whatsapp-api-client-python --no-cache-dir


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

ENV INCLUDE_TEST_ALERTS "False"

ENV MQTT_TOPIC "/redalert"


ENV GREEN_API_INSTANCE ""
ENV GREEN_API_TOKEN ""
ENV WHATSAPP_NUMBER ""



#Create working directory
RUN mkdir /opt/redalert

COPY redalert.py /opt/redalert

#Cleanup
#RUN apt remove python3-pip --yes && \
#    apt autoremove --yes && \
#    rm -rf /var/cache/*


ENTRYPOINT ["/usr/bin/python3", "/opt/redalert/redalert.py"]
