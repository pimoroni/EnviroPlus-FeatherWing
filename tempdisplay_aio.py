#----------------------------------------------------------------------------------------------------------------
'''
This code is possible because of the excellent example code provided by the Pimoroni team,
as well as the awesome online learning articles that Adafruit has worked so hard to put together!

I wanted the best of both worlds: Line graph w/ temp, humidity, and pressure values locally displayed on the
EnviroFeather's screen, as well as the ability to stream and log the readings to my Adafruit IO dashboard.

Between weeks of working on the proper ordering of code with minor adjustments, I finally got this working 99%.
Two jobs and fulltime college has kept me busy from sharing this, but here you go!

Used with a Feather M4 Express, ESP32 Coprocessor, and Enviro Feather all connected via the Proto Tripler

                                                                          ~dedSyn4ps3
'''
#----------------------------------------------------------------------------------------------------------------

#interval = 540 # full screen of reading spans 24hrs
interval = 1 # uncomment for 1 reading per second
#interval = 30 # uncomment for 1 reading per 30 seconds
#interval = 3600 # uncomment for 1 reading per hour

# the higher the threshold value the less sensitive, we've found this to be a good default through testing
mic_threshold = 3100

# the threshold for the proximity detection, the higher the less sensitive
prox_threshold = 100

# Setup

import math
import gc
import time
import board
import busio
from digitalio import DigitalInOut

import pimoroni_physical_feather_pins
from pimoroni_circuitpython_adapter import not_SMBus
from pimoroni_envirowing import gas, screen
from pimoroni_envirowing.screen import plotter
from pimoroni_ltr559 import LTR559


import displayio
import pulseio
import terminalio
from adafruit_display_text import label
import adafruit_bme280

# ESP32 SPI
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager

# Import NeoPixel Library
import neopixel

# Import Adafruit IO HTTP Client
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# ESP32 Setup
esp32_cs = DigitalInOut(board.D13)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)



spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2
)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)


# Set your Adafruit IO Username and Key in secrets.py
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Create an instance of the Adafruit IO HTTP client
io = IO_HTTP(aio_username, aio_key, wifi)

try:
    # Get the 'temperature' feed from Adafruit IO
    temperature_feed = io.get_feed("temperature")
    pressure_feed = io.get_feed("pressure")
    humidity_feed = io.get_feed("humidity")
except AdafruitIO_RequestError:
    # If no 'temperature' feed exists, create one
    temperature_feed = io.create_new_feed("temperature")
    pressure_feed = io.create_new_feed("pressure")
    humidity_feed = io.create_new_feed("humidity")


# set up the connection with the bme280
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# average global sea level pressure, for more accurate readings change this to your local sea level pressure (measured in hPa)
bme280.sea_level_pressure = 1023.50


# set up connection with the ltr559
i2c_dev = not_SMBus(I2C=i2c)
ltr559 = LTR559(i2c_dev=i2c_dev)

# setup screen
screen = screen.Screen(backlight_control=False, spi=spi)

# define our pwm pin (for changing the screen brightness)
pwm = pulseio.PWMOut(pimoroni_physical_feather_pins.pin21())

# start the screen at 50% brightness
pwm.duty_cycle = 2**15

# set up mic input
#mic = analogio.AnalogIn(pimoroni_physical_feather_pins.pin8())

# colours for the plotter are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# Setup bme280 screen plotter
# the max value is set to 70 as it is the screen height in pixels after the labels (top_space) (this is just to make a calculation later on easier)
bme280_splotter = plotter.ScreenPlotter([red, green, blue, red+green+blue], max_value=70, min_value=0, top_space=10, display=screen)

# add a colour coded text label for each reading
bme280_splotter.group.append(label.Label(terminalio.FONT, text="{:0.1f} F".format(bme280.temperature * 1.8 + 21), color=red, x=0, y=5, max_glyphs=15))
bme280_splotter.group.append(label.Label(terminalio.FONT, text="{:0.1f} hPa".format(bme280.pressure), color=green, x=50, y=5, max_glyphs=15))
bme280_splotter.group.append(label.Label(terminalio.FONT, text="{:0.1f} %".format(bme280.humidity), color=blue, x=120, y=5, max_glyphs=15))
#bme280_splotter.group.append(label.Label(terminalio.FONT, text="{:0.2f} m".format(bme280.altitude), color=red+green+blue, x=40, y=20, max_glyphs=15)) # uncomment for altitude estimation

while True:

    # take readings
    temperature = bme280.temperature * 1.8 + 21
    pressure = bme280.pressure
    humidity = bme280.humidity
    #altitude = bme280.altitude # uncomment for altitude estimation

    try:
        io.send_data(temperature_feed["key"], temperature)
        time.sleep(0.2)
        io.send_data(pressure_feed["key"], pressure)
        time.sleep(0.2)
        io.send_data(humidity_feed["key"], humidity)
        time.sleep(0.2)
    except (ValueError, RuntimeError) as e:

        wifi.reset()

    # update the line graph
    bme280_splotter.update(
        # scale to 70 as that's the number of pixels height available
        bme280_splotter.remap(temperature, 0, 125, 0, 70),
        bme280_splotter.remap(pressure, 975, 1025, 0, 70),
        bme280_splotter.remap(humidity, 0, 100, 0, 70),
        #bme280_splotter.remap(altitude, 0, 1000, 0, 70) # uncomment for altitude estimation
    )

    # update the labels
    bme280_splotter.group[1].text = "{:0.1f} F".format(temperature)
    bme280_splotter.group[2].text = "{:0.1f} hPa".format(pressure)
    bme280_splotter.group[3].text = "{:0.1f} %".format(humidity)

    time.sleep(20)
