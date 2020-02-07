"""
loggers-combined.py

Combines all the loggers into one program, recording values over a 24hr period (by default).
Allows you to switch page by waving your hand over the screen.
"""
interval = 540 # full screen of reading spans 24hrs
#interval = 1 # uncomment for 1 reading per second
#interval = 60 # uncomment for 1 reading per minute
#interval = 3600 # uncomment for 1 reading per hour

# the higher the threshold value the less sensitive, we've found this to be a good default through testing
mic_threshold = 3100 

# the threshold for the proximity detection, the higher the less sensitive
prox_threshold = 100

# Setup
import time
import math
import gc

import adafruit_bme280
import analogio
import board
import busio
import displayio
import pulseio
import terminalio
from adafruit_display_text import label

import pimoroni_physical_feather_pins
from pimoroni_circuitpython_adapter import not_SMBus
from pimoroni_envirowing import gas, screen
from pimoroni_envirowing.screen import logger
from pimoroni_ltr559 import LTR559
from pimoroni_pms5003 import PMS5003

#print("(", gc.mem_free(), ")")

# set up the connection with the bme280
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# average global sea level pressure, for more accurate readings change this to your local sea level pressure (measured in hPa)
bme280.sea_level_pressure = 1013.25

# set up the pms5003
pms5003 = PMS5003()
try:
    pms5003.read()
    is_pms5003 = True
except Exception as e:
    print(e)
    print("You probably don't have a pms5003 connected, continuing without particulate logging")
    is_pms5003 = False

# set up connection with the ltr559
i2c_dev = not_SMBus(I2C=i2c)
ltr559 = LTR559(i2c_dev=i2c_dev)

# setup screen
screen = screen.Screen(backlight_control=False)

# define our pwm pin (for changing the screen brightness)
pwm = pulseio.PWMOut(pimoroni_physical_feather_pins.pin21())

# start the screen at 50% brightness
pwm.duty_cycle = 2**15

# set up mic input
mic = analogio.AnalogIn(pimoroni_physical_feather_pins.pin8())

# colours for the logger are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# Setup bme280 screen logger
# the max value is set to 80 as it is the screen height in pixels (this is just to make a calculation later on easier)
bme280_slogger = logger.ScreenLogger([red, green, blue, red+green+blue], max_value=80, min_value=0, display=screen)

# add a colour coded text label for each reading
bme280_slogger.group.append(label.Label(terminalio.FONT, text="{:0.1f} C".format(bme280.temperature), color=red, x=0, y=5, max_glyphs=15))
bme280_slogger.group.append(label.Label(terminalio.FONT, text="{:0.1f} hPa".format(bme280.pressure), color=green, x=50, y=5, max_glyphs=15))
bme280_slogger.group.append(label.Label(terminalio.FONT, text="{:0.1f} %".format(bme280.humidity), color=blue, x=120, y=5, max_glyphs=15))
#bme280_slogger.group.append(label.Label(terminalio.FONT, text="{:0.2f} m".format(bme280.altitude), color=red+green+blue, x=40, y=20, max_glyphs=15)) # uncomment for altitude estimation

# if the pms5003 is connected
if is_pms5003:
    # Set up the pms5003 screen logger
    # the max value is set to 1000 as a nice number to work with
    pms5003_slogger = logger.ScreenLogger([green, blue, red+blue+green], max_value=1000, min_value=0, display=screen)

    # add a colour coded text label for each reading
    pms5003_slogger.group.append(label.Label(terminalio.FONT, text="PM2.5: {:d}", color=green, x=0, y=5, max_glyphs=15))
    pms5003_slogger.group.append(label.Label(terminalio.FONT, text="PM10: {:d}", color=blue, x=80, y=5, max_glyphs=15))
    #pms5003_slogger.group.append(label.Label(terminalio.FONT, text="PM1.0: {:d}", color=red, x=0, y=20, max_glyphs=15)) # uncomment to enable PM1.0 measuring

    # red line for the WHO guideline (https://en.wikipedia.org/wiki/Air_quality_guideline)
    # made in a new bitmap so it doesn't get overwritten
    pms5003_slogger.redline_bm = displayio.Bitmap(160, 1, 1)
    pms5003_slogger.redline_pl = displayio.Palette(1)
    pms5003_slogger.redline_pl[0] = red
    pms5003_slogger.redline_tg = displayio.TileGrid(pms5003_slogger.redline_bm, pixel_shader=pms5003_slogger.redline_pl, x=0, y=39)
    pms5003_slogger.group.append(pms5003_slogger.redline_tg)

# Set up the gas screen logger
# the max value is set to 3.3 as its the max voltage the feather can read
gas_slogger = logger.ScreenLogger([red, green, blue], max_value=3.3, min_value=0.5, display=screen)

# add a colour coded text label for each reading
gas_slogger.group.append(label.Label(terminalio.FONT, text="OX: {:.0f}", color=red, x=0, y=5, max_glyphs=15))
gas_slogger.group.append(label.Label(terminalio.FONT, text="RED: {:.0f}", color=green, x=80, y=5, max_glyphs=15))
gas_slogger.group.append(label.Label(terminalio.FONT, text="NH3: {:.0f}", color=blue, x=0, y=20, max_glyphs=15))

# set up the light&sound logger
lightandsound_slogger = logger.ScreenLogger([green, blue], display=screen, max_value=1)

# add a colour coded text label for each reading
lightandsound_slogger.group.append(label.Label(terminalio.FONT, text="Sound", color=green, x=0, y=5, max_glyphs=15))
lightandsound_slogger.group.append(label.Label(terminalio.FONT, text="Light", color=blue, x=80, y=5, max_glyphs=15))

# record the time that the sampling starts
last_reading = time.monotonic()
last_sec = time.monotonic()

# initialise counters at 0
reading = 0
readings = 0

# init the available pages
available_pages = {
    1: bme280_slogger,
    2: gas_slogger,
    3: lightandsound_slogger
}

# if pms5003 detected, add to available pages
if is_pms5003:
    available_pages.update({0:pms5003_slogger})

current_page = 3

# create a generator that will give the next page index, looping back to 0 once it reaches the end
def page_turner(available_pages):
    while True:
        for i in sorted(available_pages.keys()):
            yield i

# init the generator
page = page_turner(available_pages)

#print("(", gc.mem_free(), ")")

while True:
    # if 1 second has passed
    if last_sec + 1 < time.monotonic():

        # take the light reading
        lux = ltr559.get_lux()

        # take a proximity reading
        prox = ltr559.get_proximity()

        # if proximity confidence above threshold, change page
        if prox > prox_threshold:
            current_page = next(page)
            available_pages[current_page].draw(full_refresh=True)
        else:
            # change screen brightness according to the amount of light detected
            pwm.duty_cycle = int(min(lightandsound_slogger.remap(lux, 0, 400, 0, (2**16 - 1)), (2**16 - 1)))

        # if interval time has passed since last reading
        if last_reading + interval < time.monotonic():
            
            # take readings
            temperature = bme280.temperature
            pressure = bme280.pressure
            humidity = bme280.humidity
            #altitude = bme280.altitude # uncomment for altitude estimation

            # update the line graph
            bme280_slogger.update(
                # scale to 70 pixels max height to allow the labels to have dedicated screen space
                bme280_slogger.remap(temperature, 0, 50, 0, 70),
                bme280_slogger.remap(pressure, 975, 1025, 0, 70),
                bme280_slogger.remap(humidity, 0, 100, 0, 70),
                #bme280_slogger.remap(altitude, 0, 1000, 0, 70), # uncomment for altitude estimation
                draw=False
            )

            # update the labels
            bme280_slogger.group[1].text = "{:0.1f} C".format(temperature)
            bme280_slogger.group[2].text = "{:0.1f} hPa".format(pressure)
            bme280_slogger.group[3].text = "{:0.1f} %".format(humidity)
            #bme280_slogger.group[4].text = "{:0.2f} m".format(altitude) # uncomment for altitude estimation

            gc.collect()

            # take readings
            gas_reading = gas.read_all()

            # update the line graph
            # the value plotted on the graph is the voltage drop over each sensor, not the resistance, as it graphs nicer
            gas_slogger.update(
                gas_reading._OX.value * (gas_reading._OX.reference_voltage/65535),
                gas_reading._RED.value * (gas_reading._RED.reference_voltage/65535),
                gas_reading._NH3.value * (gas_reading._NH3.reference_voltage/65535),
                draw=False
            )

            # update the labels
            gas_slogger.group[1].text = "OX: {:.0f}K".format(gas_reading.oxidising/1000)
            gas_slogger.group[2].text = "RED: {:.0f}K".format(gas_reading.reducing/1000)
            gas_slogger.group[3].text = "NH3: {:.0f}K".format(gas_reading.nh3/1000)

            gc.collect()

            # get the sound readings (number of samples over the threshold / total number of samples taken) and apply a logarithm function to them to represent human hearing
            sound_level = math.log((reading/readings) + 1, 2)
            # weight the result using a -2x^3 + 3x^2 curve to emphasise changes around the midpoint (0.5)
            sound_level = (-2* sound_level**3 + 3* sound_level**2)
            # then weight the result using a x^3 - 3x^2 + 3x curve to make the results fill the graph and not sit at the bottom
            sound_level = (sound_level**3 - 3*sound_level**2 + 3*sound_level)

            # update the line graph
            lightandsound_slogger.update(
                sound_level,
                lightandsound_slogger.remap(lux, 0, 1000, 0, 1),
                draw=False
            )

            # update the labels
            lightandsound_slogger.group[1].text = "Sound: {:1.2f}".format(sound_level)
            lightandsound_slogger.group[2].text = "Light: {:.0f}".format(lux)

            gc.collect()

            if is_pms5003:
                # take readings
                pms_reading = pms5003.read()
                pm2 = pms_reading.data[1]
                pm10 = pms_reading.data[2]
                #pm1 = pms_reading.data[0] # uncomment to enable PM1.0 measuring

                # update the line graph
                pms5003_slogger.update(
                    pms5003_slogger.remap(pm2, 0, 50, 0, 1000),
                    pms5003_slogger.remap(pm10, 0, 100, 0, 1000),
                    #pms5003_slogger.remap(pm1, 0, 100, 0, 1000), # uncomment to enable PM1.0 measuring
                    draw=False
                )

                # update the labels
                pms5003_slogger.group[1].text = "PM2.5: {:d}".format(pm2)
                pms5003_slogger.group[2].text = "PM10: {:d}".format(pm10)
                #pms5003_slogger.group[3].text = "PM1.0: {:d}".format(pm1) # uncomment to enable PM1.0 measuring
                
                gc.collect()

            available_pages[current_page].draw()

            # reset the sound readings counters
            reading = 0
            readings = 0
            # record the time that this reading was taken
            last_reading = time.monotonic()

            #print("(", gc.mem_free(), ")")
        
        # update the last_sec time
        last_sec = time.monotonic()

    # take a sample of the current mic voltage
    sample = abs(mic.value - 32768)
    readings += 1
    if sample > mic_threshold:
        reading += 1
