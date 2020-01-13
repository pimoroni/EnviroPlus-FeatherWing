import time
import board
import analogio
import busio
import pulseio
import displayio
import terminalio
import adafruit_bme280
import pimoroni_physical_feather_pins
from adafruit_display_text import label
from adafruit_st7735r import ST7735R
from pimoroni_circuitpython_adapter import not_SMBus
from pimoroni_envirowing import gas
from pimoroni_envirowing.screen import logger
from pimoroni_ltr559 import LTR559
from pimoroni_pms5003 import PMS5003

class softassert():
    def __init__(self):
        self.fails = []

    def softassert(self, test, message):
        try:
            if not test():
                self.fails.append(message)
        except:
            self.fails.append(message)

softassert = softassert()

#region Screen setup
"""
This region of code is used to setup the envirowing screen with displayio
"""

spi = board.SPI() # define which spi bus the screen is on
spi.try_lock() # try to get control of the spi bus
spi.configure(baudrate=100000000) # tell the spi bus how fast it's going to run
# baudrate doesn't need to be this high in practice, it's just nice to have a quick screen refresh in this case
spi.unlock() # unlocks the spi bus so displayio can control it
tft_dc = pimoroni_physical_feather_pins.pin19() # define which pin the command line is on
tft_cs = pimoroni_physical_feather_pins.pin20() # define which pin the chip select line is on

displayio.release_displays() # release any displays that may exist from previous code run
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=pimoroni_physical_feather_pins.pin21()) # define the display bus

display = ST7735R(display_bus, width=160, height=80, colstart=26, rowstart=1, rotation=270, invert=True) # define the display (these values are specific to the envirowing's screen)

print("Screen successfully set up!")

#endregion Screen setup


i2c = board.I2C()
print("I2C Initialised!")

#region BME280 testing

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
bme280.sea_level_pressure = 1013.25
softassert.softassert(lambda: -50 <= bme280.temperature <= 50, "Temperature out of expected range")
softassert.softassert(lambda: 0 <= bme280.humidity <= 100, "Humidity out of expected range")
softassert.softassert(lambda: 850 <= bme280.pressure <= 1100, "Pressure out of expected range")
print("BME280 Tests Passed!")

#endregion BME280 testing

#region Gas Sensor testing

softassert.softassert(lambda: 0 <= gas.read_all().oxidising <= 5, "Oxidising gases reading out of expected range")
softassert.softassert(lambda: 0 <= gas.read_all().reducing <= 5, "Reducing gases reading out of expected range")
softassert.softassert(lambda: 0 <= gas.read_all().nh3 <= 5, "NH3 gases reading out of expected range")
print("Gas Sensor Tests Passed!")

#endregion Gas Sensor testing

#region Light/Prox Sensor testing

i2c_dev = not_SMBus(I2C=i2c)
ltr559 = LTR559(i2c_dev=i2c_dev)
softassert.softassert(lambda: 0 <= ltr559.get_lux() <= 30000, "Lux out of expected range")
softassert.softassert(lambda: 0 <= ltr559.get_proximity() <= 2047, "Proximity out of expected range")
print("Light/Prox Sensor Tests Passed!")

#endregion Light/Prox Sensor testing

#region Microphone testing

mic = analogio.AnalogIn(pimoroni_physical_feather_pins.pin8())
samples = list(range(20))
clap_time = 0
half_second = 500000000 # measured in nanoseconds

clap_threshold = 1000 # the higher the value the less sensitive

print("Please Double Clap. If nothing happens, there may be a problem with the Mic")
while True: # detection start
    for i in range(20): # take 20 samples of how loud it is
        samples[i] = abs(mic.value - 32768)

    if (sum(samples)/20) > clap_threshold: # if clap found

        if not clap_time + half_second >= time.monotonic_ns(): # if another clap hasn't happened in the last half second
            #print("Clap at {}".format(time.monotonic_ns()))
            clap_time = time.monotonic_ns() # update the last time a clap happened
            time.sleep(0.1)
        else: # if another clap has happened in the last half second
            print("Double Clap Detected!")
            break
print("Mic Tests Passed!")

#endregion Microphone testing

#region PM Sensor testing

pms5003 = PMS5003()
softassert.softassert(lambda: pms5003.read(), "Problem with reading data from PMS5003")
print("PMS5003 Tests Passed!")

#endregion PM Sensor testing

if len(softassert.fails) == 0:
    print("All tests passed!")
else:
    print("These tests failed:")
    for i in softassert.fails:
        print(i)

while True:
    time.sleep(1)