"""
logger-light&sound.py

Logs the levels of light and noise levels over a 24hr period (by default).
"""

interval = 540 # full screen of reading spans 24hrs
#interval = 1 # uncomment for 1 reading per second
#interval = 60 # uncomment for 1 reading per minute
#interval = 3600 # uncomment for 1 reading per hour

# the higher the threshold value the less sensitive, we've found this to be a good default through testing
threshold = 3100 

import time
import math

import analogio
import pulseio
import terminalio

from adafruit_display_text import label

import pimoroni_physical_feather_pins
from pimoroni_circuitpython_adapter import not_SMBus
from pimoroni_envirowing import screen
from pimoroni_envirowing.screen import logger
from pimoroni_ltr559 import LTR559

# colours for the logger are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# set up the mic
mic = analogio.AnalogIn(pimoroni_physical_feather_pins.pin8())

# set up the screen
screen = screen.Screen(backlight_control=False)

# set up connection with the sensor
i2c_dev = not_SMBus()
ltr559 = LTR559(i2c_dev=i2c_dev)

# define our pwm pin (for changing the screen brightness)
pwm = pulseio.PWMOut(pimoroni_physical_feather_pins.pin21())

# start the screen at 50% brightness
pwm.duty_cycle = 2**15

# set up the logger
slogger = logger.ScreenLogger([green, blue], display=screen, max_value=1)

# add a colour coded text label for each reading
slogger.group.append(label.Label(terminalio.FONT, text="Sound", color=green, x=0, y=5))
slogger.group.append(label.Label(terminalio.FONT, text="Light", color=blue, x=80, y=5))

# record the time that the sampling starts
last_reading = time.monotonic()

# initialise counters at 0
reading = 0
readings = 0

while True:
    # if interval time has passed since last reading
    if last_reading + interval < time.monotonic():
        # take the light reading
        lux = ltr559.get_lux()
        # get the sound readings (number of samples over the threshold / total number of samples taken) and apply a logarithm function to them to represent human hearing
        sound_level = math.log((reading/readings) + 1, 2)
        # weight the result using a -2x^3 + 3x^2 curve to emphasise changes around the midpoint (0.5)
        sound_level = (-2* sound_level**3 + 3* sound_level**2)

        # update the line graph
        slogger.update(
            sound_level,
            slogger.remap(lux, 0, 1000, 0, 1)
        )

        # update the labels
        slogger.group[1] = label.Label(terminalio.FONT, text="Sound: {:1.2f}".format(sound_level), color=green, x=0, y=5)
        slogger.group[2] = label.Label(terminalio.FONT, text="Light: {:.0f}".format(lux), color=blue, x=80, y=5)

        # change screen brightness according to the amount of light detected
        pwm.duty_cycle = int(min(slogger.remap(lux, 0, 400, 0, (2**16 - 1)), (2**16 - 1)))

        # reset the sound readings counters
        reading = 0
        readings = 0
        # record the time that this reading was taken
        last_reading = time.monotonic()

    # take a sample of the current mic voltage
    sample = abs(mic.value - 32768)
    readings += 1
    if sample > threshold:
        reading += 1