# mqtt-prometheus-adapter

Adapter to subscribe to mqtt topics and log them into prometheus.

## Configuration

In order to use the adapter, please update the config.yml:
- `host`: Server ip / url
- `port`: MQTT Port e.g. 1883
- `topics`: Export name of datapoints
    - `path`: Topic name e.g. sensors/temperature
    - `conversion`: optional if you need to extract values from a string
        - `re_pattern`: Regular Expressions filter pattern
        - `exports`: names of the datapoints as array
            - `mapping`: string to number mapping pairs‚
    - `type`: gauge (default), counter
    - `filter`: regular expressions filter pattern (only for counter)
- `polling`: Send payload to topics every n seconds
    - `interval`: Send interval in seconds
    - `topics`: Array of key-value pairs (- topic: payload)
- `log_topic_updates`: If true, print all data received on subscribed topics

## How to compile

In some cases you might need to export a .docker precompiled image:

- Compile: `sudo docker buildx build --platform linux/amd64/v2 --tag mqtt-prometheus-adapter .`
- Save to file: `sudo docker save -o mqtt-prometheus-adapter.docker mqtt-prometheus-adapter`
- Edit read/write rights (optional): `sudo chmod 777 mqtt-prometheus-adapter.docker`

You can find more informations about compiling for different plattforms [here](https://docs.docker.com/build/building/multi-platform/).

## Resources

- [Build your Python image](https://docs.docker.com/language/python/build-images/)
- [Prometheus-Client Python](https://github.com/prometheus/client_python)
- [Paho MQTT Client](https://pypi.org/project/paho-mqtt/)
