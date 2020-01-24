"""
logger-particulate.py

Logs the levels of particulate matter over a 24hr period (by default).
A red line is displayed marking the WHO guideline, the max value that the average over 24hrs must not exceed.
Readings are scaled such that both particulates guideline values are represented by the same red line.
PM1.0 readings are disabled by default as there is no standard to compare to at this time

"""

interval = 540 # full screen of reading spans 24hrs
#interval = 1 # uncomment for 1 reading per second
#interval = 60 # uncomment for 1 reading per minute
#interval = 3600 # uncomment for 1 reading per hour

import time 

from pimoroni_pms5003 import PMS5003
from pimoroni_envirowing.screen import logger

import terminalio
from adafruit_display_text import label

# colours for the logger are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# set up the sensor
pms5003 = PMS5003()

# Set up the logger
# the max value is set to 1000 as a nice number to work with
slogger = logger.ScreenLogger([green, blue, red+blue+green, red], max_value=1000, min_value=0)

# add a colour coded text label for each reading
slogger.group.append(label.Label(terminalio.FONT, text="PM2.5: {:d}", color=green, x=0, y=5))
slogger.group.append(label.Label(terminalio.FONT, text="PM10: {:d}", color=blue, x=80, y=5))
#slogger.group.append(label.Label(terminalio.FONT, text="PM1.0: {:d}", color=red, x=0, y=20)) # uncomment to enable PM1.0 measuring

# red line for the WHO guideline (https://en.wikipedia.org/wiki/Air_quality_guideline)
for i in range(slogger.bitmap.width):
    slogger.bitmap[i, 39] = 4


while True:
    # take readings
    reading = pms5003.read()
    pm2 = reading.data[1]
    pm10 = reading.data[2]
    #pm1 = reading.data[0] # uncomment to enable PM1.0 measuring

    # update the line graph
    slogger.update(
        slogger.remap(pm2, 0, 50, 0, 1000),
        slogger.remap(pm10, 0, 100, 0, 1000),
        #slogger.remap(pm1, 0, 100, 0, 1000) # uncomment to enable PM1.0 measuring
    )

    # update the labels
    slogger.group[1] = label.Label(terminalio.FONT, text="PM2.5: {:d}".format(pm2), color=green, x=0, y=5)
    slogger.group[2] = label.Label(terminalio.FONT, text="PM10: {:d}".format(pm10), color=blue, x=80, y=5)
    #slogger.group[3] = label.Label(terminalio.FONT, text="PM1.0: {:d}".format(pm1), color=red, x=0, y=20)) # uncomment to enable PM1.0 measuring

    time.sleep(interval)