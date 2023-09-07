# mqtt-prometheus-adapter

Adapter to subscribe to mqtt topics and log them into prometheus.

## Configuration

In order to use the adapter, please update the config.yml:
- Host: Server ip / url
- Port: MQTT Port e.g. 1883
- Topics: Export name of datapoints
    - path: Topic name e.g. sensors/temperature
    - conversion: optional if you need to extract values from a string
        - re_pattern: Regular Expressions filter pattern
        - exports: names of the datapoints as array

## Resources

[Build your Python image](https://docs.docker.com/language/python/build-images/)
