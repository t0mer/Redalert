#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import paho.mqtt.client as mqtt
import urllib3
import os
from loguru import logger
import time
import codecs
import apprise
import json
from whatsapp_api_client_python import API

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
NOTIFIERS = os.getenv("NOTIFIERS")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "/redalert")
INCLUDE_TEST_ALERTS = os.getenv("INCLUDE_TEST_ALERTS")
GREEN_API_INSTANCE = os.getenv("GREEN_API_INSTANCE")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")
# reader = codecs.getreader('utf-8')

logger.info("Monitoring alerts for :" + region)


#Setting Request Headers
http = urllib3.PoolManager()
_headers = {'Referer':'https://www.oref.org.il/','User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",'X-Requested-With':'XMLHttpRequest'}
url= 'https://www.oref.org.il/WarningMessages/alert/alerts.json'
if debug == 'True':
   url = 'http://localhost/alerts.json'

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


alerts = [0]

# Setting apprise Job Manager
apobj = apprise.Apprise()

#Setting up MqttClient
client = mqtt.Client("redalert")
client.username_pw_set(user,passw)
client.on_connect=on_connect
client.on_disconnect=on_disconnect

client.loop_start()
logger.info("Connecting to broker")
mqtt.Client.connected_flag=False#create flag in class
client.connect(server, keepalive=3600)

while not client.connected_flag: #wait in loop
    logger.info("In wait loop")
    time.sleep(1)
logger.info("in Main Loop")
client.loop_stop()    #Stop loop 


if len(NOTIFIERS)!=0:
    logger.info("Setting Apprise Alert")
    jobs=NOTIFIERS.split()
    for job in jobs:
        logger.info("Adding: " + job)
        apobj.add(job)


def alarm_on(data):
    client.publish(MQTT_TOPIC + "/data",str(data["data"]),qos=0,retain=False)
    client.publish(MQTT_TOPIC,'on',qos=0,retain=False)
    if len(NOTIFIERS)!=0:
        logger.info("Alerting using Notifires")
        apobj.notify(
            body='באזורים הבאים: \r\n ' + ', '.join(data["data"]).replace(',','\r\n') + '\r\n' + str(data["desc"] ),
            title=str(data["title"]),
            )
    try:
        if GREEN_API_INSTANCE and GREEN_API_TOKEN:
            greenAPI = API.GreenAPI(GREEN_API_INSTANCE, GREEN_API_TOKEN)
            greenAPI.sending.sendMessage(WHATSAPP_NUMBER, 'באזורים הבאים: \r\n ' + ', '.join(data["data"]).replace(',','\r\n') + '\r\n' + str(data["desc"] ))
    except Exception as e:
        logger.error(f"Error sending whatsapp message. \n {str(e)}")

def alarm_off():
    client.publish(MQTT_TOPIC + "/alarm",'off',qos=0,retain=False)
    client.publish(MQTT_TOPIC,"No active alerts",qos=0,retain=False)

def is_test_alert(alert):
    # if includes, all alerts are treated as not test
    return INCLUDE_TEST_ALERTS == 'False' and ('בדיקה' in alert['data'] or 'בדיקה מחזורית' in alert['data'])

def monitor():
  #start the timer
  threading.Timer(1, monitor).start()
  #Check if data contains alert data
  try:
      r = http.request('GET',url,headers=_headers)
      r.encoding = 'utf-8'
      alert_data = r.data.decode('utf-8-sig').strip("/n").strip()
      if alert_data != '':
          alert = json.loads(alert_data)
          if region in alert["data"] or region=="*":
              if alert["id"] not in alerts and not is_test_alert(alert):
                  alerts.append(alert["id"])
                  alarm_on(alert)
                  logger.info(str(alert))
      else:
         alarm_off()
  except Exception as ex:
         logger.error(str(ex))
  finally:
     r.release_conn()

if __name__ == '__main__':
   monitor()
