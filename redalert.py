import threading
import paho.mqtt.client as mqtt
import urllib3
import os
from loguru import logger

#mqtt connection Params
server = os.getenv('MQTT_HOST')
#Default port is 1883
port = int(os.getenv('MQTT_PORT'))
user = os.getenv('MQTT_USER')
passw = os.getenv('MQTT_PASS')
debug = os.getenv('DEBUG_MODE')


#Setting Request Headers
http = urllib3.PoolManager()
_headers = {'Referer':'https://www.oref.org.il/','User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",'X-Requested-With':'XMLHttpRequest'}
url= 'https://www.oref.org.il/WarningMessages/alert/alerts.json'
if debug == 'True':
   url = 'https://techblog.co.il/alerts.json'


#Setting up MqttClient
client = mqtt.Client("redalert")
client.username_pw_set(user,passw)
logger.info('#########################')
logger.info("Using Username: " + user)
logger.info("Ussing Password: " + passw)
client.connect(server)
logger.info("Using Server: " + server)
logger.info('#########################')

def monitor():
  #start the timer
  threading.Timer(1, monitor).start()
  #Check for Alerts
  r = http.request('GET',url,headers=_headers)
  #Check if data contains alert data
  try:
      if r.data != b'': #if there as alert, publish it to HA using Mqtt
         result=client.publish("/redalert/",r.data,qos=0,retain=False)
         logger.info(str(r.data)
  except Exception as ex:
         logger.error(str(e))


monitor()
