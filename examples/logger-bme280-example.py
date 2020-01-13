import adafruit_bme280, board, busio
from pimoroni_envirowing.screen import logger

import terminalio
from adafruit_display_text import label

import time

# colours for the logger are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# set up the connection with the sensor
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# average global sea level pressure, for more accurate readings change this to your local sea level pressure (measured in hPa)
bme280.sea_level_pressure = 1013.25

# the max value is set to 1000 as a nice number to work with
slogger = logger.ScreenLogger([red, green, blue, red+green+blue], max_value=1000, min_value=0)

# add a colour coded text label for each reading
slogger.group.append(label.Label(terminalio.FONT, text="%0.1f C" % bme280.temperature, color=red, x=0, y=5))
slogger.group.append(label.Label(terminalio.FONT, text="%0.1f hPa" % bme280.pressure, color=green, x=40, y=5))
slogger.group.append(label.Label(terminalio.FONT, text="%0.1f %%" % bme280.humidity, color=blue, x=0, y=20))
slogger.group.append(label.Label(terminalio.FONT, text="%0.2f m" % bme280.altitude, color=red+green+blue, x=40, y=20))

# define a remap function to scale a value from an old range to a new range, preserving ratio
def remap(Value, OldMin,OldMax, NewMin, NewMax):
    return (((Value - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin


while True:
    # take readings
    temperature = bme280.temperature
    pressure = bme280.pressure
    humidity = bme280.humidity
    altitude = bme280.altitude

    # update the line graph
    slogger.update(
        remap(temperature, 0, 50, 0, 1000),
        remap(pressure, 975, 1025, 0, 1000),
        remap(humidity, 0, 100, 0, 1000),
        remap(altitude, 0, 1000, 0, 1000)
    )

    # update the labels
    slogger.group[1] = (label.Label(terminalio.FONT, text="%0.1f C" % temperature, color=red, x=0, y=5))
    slogger.group[2] = (label.Label(terminalio.FONT, text="%0.1f hPa" % pressure, color=green, x=40, y=5))
    slogger.group[3] = (label.Label(terminalio.FONT, text="%0.1f %%" % humidity, color=blue, x=0, y=20))
    slogger.group[4] = (label.Label(terminalio.FONT, text="%0.2f m" % altitude, color=red+green+blue, x=40, y=20))

    time.sleep(1)