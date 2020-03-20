"""
plotter-bme280.py

Logs the temperature, humidity and pressure over 24hrs (by default)
"""

interval = 540 # full screen of reading spans 24hrs
#interval = 1 # uncomment for 1 reading per second
#interval = 60 # uncomment for 1 reading per minute
#interval = 3600 # uncomment for 1 reading per hour

import time

import adafruit_bme280, board, busio
from pimoroni_envirowing.screen import plotter

import terminalio
from adafruit_display_text import label

# colours for the plotter are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# set up the connection with the sensor
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# average global sea level pressure, for more accurate readings change this to your local sea level pressure (measured in hPa)
bme280.sea_level_pressure = 1013.25

# the max value is set to 70 as it is the screen height in pixels after the labels (top_space) (this is just to make a calculation later on easier)
splotter = plotter.ScreenPlotter([red, green, blue, red+green+blue], max_value=70, min_value=0, top_space=10)

# add a colour coded text label for each reading
splotter.group.append(label.Label(terminalio.FONT, text="{:0.1f} C".format(bme280.temperature), color=red, x=0, y=5, max_glyphs=15))
splotter.group.append(label.Label(terminalio.FONT, text="{:0.1f} hPa".format(bme280.pressure), color=green, x=50, y=5, max_glyphs=15))
splotter.group.append(label.Label(terminalio.FONT, text="{:0.1f} %".format(bme280.humidity), color=blue, x=120, y=5, max_glyphs=15))
#splotter.group.append(label.Label(terminalio.FONT, text="{:0.2f} m".format(bme280.altitude), color=red+green+blue, x=40, y=20, max_glyphs=15)) # uncomment for altitude estimation


while True:
    # take readings
    temperature = bme280.temperature
    pressure = bme280.pressure
    humidity = bme280.humidity
    #altitude = bme280.altitude # uncomment for altitude estimation

    # update the line graph
    splotter.update(
        # scale to 70 as that's the number of pixels height available
        splotter.remap(temperature, 0, 50, 0, 70),
        splotter.remap(pressure, 975, 1025, 0, 70),
        splotter.remap(humidity, 0, 100, 0, 70),
        #splotter.remap(altitude, 0, 1000, 0, 70) # uncomment for altitude estimation
    )

    # update the labels
    splotter.group[1].text = "{:0.1f} C".format(temperature)
    splotter.group[2].text = "{:0.1f} hPa".format(pressure)
    splotter.group[3].text = "{:0.1f} %".format(humidity)
    #splotter.group[4].text = "{:0.2f} m".format(altitude) # uncomment for altitude estimation

    time.sleep(interval)