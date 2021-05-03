"""
plotter_scd30.py

Logs the level of carbon dioxide (CO2) in ppm over a 24hr period (by default).

"""

interval = 540 # full screen of reading spans 24hrs
#interval = 1 # uncomment for 1 reading per second
#interval = 60 # uncomment for 1 reading per minute
#interval = 3600 # uncomment for 1 reading per hour

import time

import board
import terminalio
from adafruit_display_text import label
from adafruit_scd30 import SCD30
from pimoroni_envirowing.screen import plotter


# colours for the plotter are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# set up the sensor
scd30 = SCD30(board.I2C())

# The SCD-30 is more accurate if given local air pressure in mb (hPa)
# which is available from the BME280 on the Enviro+ FeatherWing
# The altitude in metres is a less accurate way of compensating for pressure
# The altitude is remembered if the power is removed and is best set
# only when needed to avoid wear on SCD-30 NVRAM
#scd30.ambient_pressure = 1021
#scd30.altitude = 123

# Set up the plotter
splotter = plotter.ScreenPlotter([green], max_value=3000, min_value=0, top_space=10)

# add a colour coded text label for each reading
splotter.group.append(label.Label(terminalio.FONT,
                                  text="CO2: {:.0f} ppm",
                                  color=green, x=0, y=5, max_glyphs=15))

while True:
    # take readings
    co2ppm = scd30.CO2
    splotter.update(co2ppm)
    splotter.group[1].text = "CO2: {:.0f} ppm".format(co2ppm)

    time.sleep(interval)
