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
