# Red Alert Docker
__________________________________________

Ubuntu based image running python script that reads json from [Oref Website](https://www.oref.org.il/). <br/>
and publishes it over MQTT Protocol.

## Base Image
`From ubuntu:18.04` described [here](https://hub.docker.com/_/ubuntu).


## 18/05/2021 Major update
Thanks to the amazing work of [@caronc](https://github.com/caronc) on the [apprise](https://github.com/caronc/apprise) 
you can now send notification using variety of notification channels, like:
* Telegram - [tgram://bottoken/ChatID](https://github.com/caronc/apprise/wiki/Notify_telegram)
* Home-Assistant - [hassio://user@hostname/accesstoken](https://github.com/caronc/apprise/wiki/Notify_homeassistant)
* IFTTT - [ifttt://{WebhookID}@{Event}/](https://github.com/caronc/apprise/wiki/Notify_ifttt)
* Slack - [slack://TokenA/TokenB/TokenC/Channel](https://github.com/caronc/apprise/wiki/Notify_slack)
* Microsoft Teams - [msteams://TokenA/TokenB/TokenC/](https://github.com/caronc/apprise/wiki/Notify_msteams)

And much musch more. you can find it all on the project [Wiki](https://github.com/caronc/apprise/wiki).

This update also contains:
* Reducing the length of the data sends over the Mqtt prorocol, it is now contains regions only.
* Added detaild log.
* Fixed the bug that causing sendind multiple alerts.

## Image configuration
### Enviroment variables
- *MQTT_HOST*</br>
used for setting the MQTT Broker address, default value is `127.0.0.1`.
- *MQTT_PORT*</br>
used for setting the MQTT Broker Port, default value is `1883`.
- *MQTT_USER*</br>
used for setting the MQTT Broker Username, default value is `user`.
- *MQTT_PASS*</br>
used for setting the MQTT Broker Password, default value is `password`.
- *DEBUG_MODE*</br>
used for setting the script to run in test mode wich will read json from test url.
- *INCLUDE_TEST_ALERTS*</br>
used to show pikud ha oref tests, default is False.
- *REGION*</br>
used for setting the region for monitoring. default is * (any)
- *NOTIFIERS*</br>
use apprise notification. you can use multiple notifiers separated by space python for example: </br>
```tgram://bottoken/ChatID hassio://user@hostname/accesstoken slack://TokenA/TokenB/TokenC/Channel```
- *MQTT_TOPIC*</br>
Custom MQTT Topic. default value is `/redalert`


## Usage
### Run from hub
#### docker run from hub
```text
docker run  -e MQTT_HOST="broker ip / fqdn" -e MQTT_PORT="1883" -e MQTT_USER="username" -e MQTT_PASS="password" -e DEBUG_MODE="False" -e REGION="*" --name redalert techblog/redalert:latest
```

#### docker-compose from hub
```yaml
version: "3.6"
services:
  redalert:
    image: techblog/redalert
    container_name: redalert
    restart: always
    environment:
      - MQTT_HOST=[Broker Address]
      - MQTT_USER=[Broker Username]
      - MQTT_PASS=[Broker Password]
      - DEBUG_MODE=False
      - REGION=[* for any or region name)
      - NOTIFIERS=[Apprise notifiers]
      - INCLUDE_TEST_ALERTS=[False|True]
    restart: unless-stopped
```
### Adding Sensor in Home-Assistant
#### Get full json (including date and id)
```yaml
  - platform: mqtt
    name: "Red Alert"
    state_topic: "/redalert/"
    # unit_of_measurement: '%'
    icon: fas:broadcast-tower
    value_template: "{{ value_json }}"
    qos: 1
```

#### Get json with alert areas only
```yaml
  - platform: mqtt
    name: "Red Alert"
    state_topic: "/redalert/"
    # unit_of_measurement: '%'
    icon: fas:broadcast-tower
    value_template: "{{ value_json.data }}"
    qos: 1
```
#### In some case the above snipet code will not work for you, you can try that:
```yaml
  - platform: mqtt
    name: "Red Alert"
    state_topic: "/redalert/"
    # unit_of_measurement: '%'
    icon: fas:broadcast-tower
    value_template: "{{ value }}"
    json_attributes_topic: "/redalert/data"
    json_attributes_template: "{{ value_json | tojson }}"
    qos: 1
```

#### Alaram state (Value will be on/off)
```yaml
  - platform: mqtt
    name: "Red Alert"
    state_topic: "/redalert/alarm"
    icon: fas:broadcast-tower
    value_template: "{{ value_json }}"
    qos: 1
```
