# Adafruit IO Example

This project uses an AirLift FeatherWing in addition to the Enviro+ to transfer data via WiFi to Adafruit IO.

Note: This project does not work with the PMS5003 sensor, since it shares pins with the AirLift WiFi board.

For more information about Adafruit IO setup, see: https://learn.adafruit.com/adafruit-io-basics-airlift/adafruit-io-setup

## Requirements

### Secrets

You will need to sign up with Adafruit IO: https://io.adafruit.com/

Once signed in, click the "Adafruit IO Key" link in the top right to find your key.

You will also need to know your WiFi SSD and password.

These details should go into a new file, `secrets.py`, with the following format:

```python
secrets = {
    'ssid' : 'YOUR ACCESSPOINT',
    'password' : 'ACCESSPOINT PASSWORD',
    'timezone' : "America/New_York", # http://worldtimeapi.org/timezones
    'aio_username' : 'YOUR AIO USERNAME',
    'aio_key' : 'YOUR AIO KEY',
    }
```

### Hardware

* Adafruit Feather M4 Express
* Adafruit AirLift WiFi FeatherWing (ESP32 Coprocessor)
* Enviro+ FeatherWing

### Libraries

In addition to the libraries required by Enviro+, you will also need:

* `adafruit_esp32spi` (directory)
* `adafruit_io` (directory)
* `adafruit_requests` (.mpy file)
* `neopixel` (.mpy file)
