# Red Alert Docker
__________________________________________

Ubuntu based image running python script that reads json from [Oref Website](https://www.oref.org.il/). <br/>
and publishes it over MQTT Protocol.

## Base Image
`From ubuntu:18.04` described [here](https://hub.docker.com/_/ubuntu).

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

## Usage
### Run from hub
#### docker run from hub
```text
docker run  -e MQTT_HOST="broker ip / fqdn" -e MQTT_PORT="1883" -e MQTT_USER="username" -e MQTT_PASS="password" -e DEBUG_MODE="False"  --name redalert techblog/redalert:latest
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


