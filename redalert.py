#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import paho.mqtt.client as mqtt
import urllib3
import os
from loguru import logger
import time
import codecs
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'C.UTF-8'

#mqtt connection Params
server = os.getenv('MQTT_HOST')
#Default port is 1883
port = int(os.getenv('MQTT_PORT'))
user = os.getenv('MQTT_USER')
passw = os.getenv('MQTT_PASS')
debug = os.getenv('DEBUG_MODE')
region = os.getenv('REGION')

reader = codecs.getreader('utf-8')

logger.info("Monitoring alert for :" + region)


#Setting Request Headers
http = urllib3.PoolManager()
_headers = {'Referer':'https://www.oref.org.il/','User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",'X-Requested-With':'XMLHttpRequest'}
url= 'https://www.oref.org.il/WarningMessages/alert/alerts.json'
if debug == 'True':
   url = 'https://techblog.co.il/alerts.json'

#Check Connection Status
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        logger.info("connected OK Returned code=" + str(rc))
    else:
       if rc==1:
          logger.error("Connection refused – incorrect protocol version")
       if rc==2:
           logger.error("Connection refused – invalid client identifier")
       if rc==3:
           logger.error("Connection refused – server unavailable")
       if rc==4:
           logger.error("Connection refused – bad username or password")
       if rc==5:
           logger.error("Connection refused – not authorised")
        
def on_disconnect(client, userdata, rc):
    logger.info("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True
    client.connect(server)


def on_log(client, userdata, level, buf):
    logger.inf(buf)


#Setting up MqttClient
client = mqtt.Client("redalert")

#Setting Credentials
client.username_pw_set(user,passw)

#Setting Callback
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_log=on_log # set client logging
#Connetcting
client.loop_start()
logger.info("Connecting to broker")
mqtt.Client.connected_flag=False#create flag in class
client.connect(server, keepalive=3600)

while not client.connected_flag: #wait in loop
    logger.info("In wait loop")
    time.sleep(1)
logger.info("in Main Loop")
client.loop_stop()    #Stop loop 

def monitor():
  #start the timer
  threading.Timer(1, monitor).start()
  #Check for Alerts
  r = http.request('GET',url,headers=_headers)
  r.encoding = 'utf-8'
  #Check if data contains alert data
  try:
      if r.data != b'': #if there as alert, publish it to HA using Mqtt
         if region in r.data.decode('utf-8') or region=="*":
            result=client.publish("/redalert/",r.data,qos=0,retain=False)
            client.publish("/redalert/alarm",'on',qos=0,retain=False)
            
      else:
         client.publish("/redalert/alarm",'off',qos=0,retain=False)
         result=client.publish("/redalert/",'',qos=0,retain=False)
  except Exception as ex:
         logger.error(str(ex))
  finally:
     r.release_conn()
if __name__ == '__main__':
   monitor()
