"""
logger-bme280-example.py

Logs the temperature, humidity and pressure over 24hrs (by default)
"""

interval = 540 # full screen of reading spans 24hrs
#interval = 1 # uncomment for 1 reading per second
#interval = 60 # uncomment for 1 reading per minute
#interval = 3600 # uncomment for 1 reading per hour

import time

import adafruit_bme280, board, busio
from pimoroni_envirowing.screen import logger

import terminalio
from adafruit_display_text import label

# colours for the logger are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# set up the connection with the sensor
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# average global sea level pressure, for more accurate readings change this to your local sea level pressure (measured in hPa)
bme280.sea_level_pressure = 1013.25

# the max value is set to 80 as it is the screen height in pixels (this is just to make a calculation later on easier)
slogger = logger.ScreenLogger([red, green, blue, red+green+blue], max_value=80, min_value=0)

# add a colour coded text label for each reading
slogger.group.append(label.Label(terminalio.FONT, text="%0.1f C" % bme280.temperature, color=red, x=0, y=5))
slogger.group.append(label.Label(terminalio.FONT, text="%0.1f hPa" % bme280.pressure, color=green, x=50, y=5))
slogger.group.append(label.Label(terminalio.FONT, text="%0.1f %%" % bme280.humidity, color=blue, x=120, y=5))
#slogger.group.append(label.Label(terminalio.FONT, text="%0.2f m" % bme280.altitude, color=red+green+blue, x=40, y=20)) # uncomment for altitude estimation


while True:
    # take readings
    temperature = bme280.temperature
    pressure = bme280.pressure
    humidity = bme280.humidity
    #altitude = bme280.altitude # uncomment for altitude estimation

    # update the line graph
    slogger.update(
        # scale to 70 pixels max height to allow the labels to have dedicated screen space
        slogger.remap(temperature, 0, 50, 0, 70),
        slogger.remap(pressure, 975, 1025, 0, 70),
        slogger.remap(humidity, 0, 100, 0, 70),
        #slogger.remap(altitude, 0, 1000, 0, 70) # uncomment for altitude estimation
    )

    # update the labels
    slogger.group[1] = (label.Label(terminalio.FONT, text="%0.1f C" % temperature, color=red, x=0, y=5))
    slogger.group[2] = (label.Label(terminalio.FONT, text="%0.1f hPa" % pressure, color=green, x=50, y=5))
    slogger.group[3] = (label.Label(terminalio.FONT, text="%0.1f %%" % humidity, color=blue, x=120, y=5))
    #slogger.group[4] = (label.Label(terminalio.FONT, text="%0.2f m" % altitude, color=red+green+blue, x=40, y=20)) # uncomment for altitude estimation

    time.sleep(interval)