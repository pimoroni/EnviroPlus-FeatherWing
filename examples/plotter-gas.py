"""
plotter-gas.py

Logs the levels of different gases over 24hrs (by default)
"""

interval = 540 # full screen of reading spans 24hrs
#interval = 1 # uncomment for 1 reading per second
#interval = 60 # uncomment for 1 reading per minute
#interval = 3600 # uncomment for 1 reading per hour

import time

from pimoroni_envirowing import gas
from pimoroni_envirowing.screen import plotter

import terminalio
from adafruit_display_text import label

# colours for the plotter are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# the max value is set to 3.3 as its the max voltage the feather can read
splotter = plotter.ScreenPlotter([red, green, blue], max_value=3.3, min_value=0.5, top_space=10)

# add a colour coded text label for each reading
splotter.group.append(label.Label(terminalio.FONT, text="OX:{}", color=red, x=0, y=5, max_glyphs=15))
splotter.group.append(label.Label(terminalio.FONT, text="RED:{}", color=green, x=50, y=5, max_glyphs=15))
splotter.group.append(label.Label(terminalio.FONT, text="NH3:{}", color=blue, x=110, y=5, max_glyphs=15))

# from https://stackoverflow.com/a/49955617
def human_format(num, round_to=0):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num = round(num / 1000.0, round_to)
    return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

while True:
    #take readings
    reading = gas.read_all()

    # update the line graph
    # the value plotted on the graph is the voltage drop over each sensor, not the resistance, as it graphs nicer
    splotter.update(
        reading._OX.value * (reading._OX.reference_voltage/65535),
        reading._RED.value * (reading._RED.reference_voltage/65535),
        reading._NH3.value * (reading._NH3.reference_voltage/65535)
    )

    # update the labels
    splotter.group[1].text = "OX:{}".format(human_format(reading.oxidising))
    splotter.group[2].text = "RED:{}".format(human_format(reading.reducing))
    splotter.group[3].text = "NH3:{}".format(human_format(reading.nh3))
    
    time.sleep(interval)
