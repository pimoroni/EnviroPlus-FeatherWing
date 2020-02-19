"""
plotter-particulate.py

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
from pimoroni_envirowing.screen import plotter

import terminalio, displayio
from adafruit_display_text import label

# colours for the plotter are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# set up the sensor
pms5003 = PMS5003()

# Set up the plotter
# the max value is set to 1000 as a nice number to work with
splotter = plotter.ScreenPlotter([green, blue, red+blue+green], max_value=1000, min_value=0)

# add a colour coded text label for each reading
splotter.group.append(label.Label(terminalio.FONT, text="PM2.5: {:d}", color=green, x=0, y=5, max_glyphs=15))
splotter.group.append(label.Label(terminalio.FONT, text="PM10: {:d}", color=blue, x=80, y=5, max_glyphs=15))
#splotter.group.append(label.Label(terminalio.FONT, text="PM1.0: {:d}", color=red, x=0, y=20, max_glyphs=15)) # uncomment to enable PM1.0 measuring

# red line for the WHO guideline (https://en.wikipedia.org/wiki/Air_quality_guideline)
# made in a new bitmap so it doesn't get overwritten
splotter.redline_bm = displayio.Bitmap(160, 1, 1)
splotter.redline_pl = displayio.Palette(1)
splotter.redline_pl[0] = red
splotter.redline_tg = displayio.TileGrid(splotter.redline_bm, pixel_shader=splotter.redline_pl, x=0, y=39)
splotter.group.append(splotter.redline_tg)


while True:
    # take readings
    reading = pms5003.read()
    pm2 = reading.data[1]
    pm10 = reading.data[2]
    #pm1 = reading.data[0] # uncomment to enable PM1.0 measuring

    # update the line graph
    splotter.update(
        splotter.remap(pm2, 0, 50, 0, 1000),
        splotter.remap(pm10, 0, 100, 0, 1000),
        #splotter.remap(pm1, 0, 100, 0, 1000) # uncomment to enable PM1.0 measuring
    )

    # update the labels
    splotter.group[1].text = "PM2.5: {:d}".format(pm2)
    splotter.group[2].text = "PM10: {:d}".format(pm10)
    #splotter.group[3].text = "PM1.0: {:d}".format(pm1) # uncomment to enable PM1.0 measuring

    time.sleep(interval)