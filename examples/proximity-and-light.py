import time
from pimoroni_ltr559 import LTR559
from pimoroni_circuitpython_adapter import not_SMBus

#region Screen setup
"""
This region of code is used to setup the envirowing screen with displayio
"""

import board, time
import pimoroni_physical_feather_pins
import displayio, pulseio
from adafruit_st7735r import ST7735R

spi = board.SPI() # define which spi bus the screen is on
spi.try_lock() # try to get control of the spi bus
spi.configure(baudrate=100000000) # tell the spi bus how fast it's going to run
# baudrate doesn't need to be this high in practice, it's just nice to have a quick screen refresh in this case
spi.unlock() # unlocks the spi bus so displayio can control it
tft_dc = pimoroni_physical_feather_pins.pin19() # define which pin the command line is on
tft_cs = pimoroni_physical_feather_pins.pin20() # define which pin the chip select line is on

displayio.release_displays() # release any displays that may exist from previous code run
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs) # define the display bus

display = ST7735R(display_bus, width=160, height=80, colstart=26, rowstart=1, rotation=270, invert=True) # define the display (these values are specific to the envirowing's screen)

#endregion Screen setup

# define a remap function to scale a value from an old range to a new range, preserving ratio
def remap(Value, OldMin,OldMax, NewMin, NewMax):
    return (((Value - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

# set up connection with the sensor
i2c_dev = not_SMBus()
ltr559 = LTR559(i2c_dev=i2c_dev)

# define our pwm pin (for changing the screen brightness)
pwm = pulseio.PWMOut(pimoroni_physical_feather_pins.pin21())

try:
    while True:
        # take readings
        lux = ltr559.get_lux()
        prox = ltr559.get_proximity()

        # change screen brightness according to the amount of light detected
        pwm.duty_cycle = int(min(remap(lux, 0, 400, 0, (2**16 - 1)), (2**16 - 1)))

        print("Lux: {:06.2f}, Proximity: {:04d}".format(lux, prox))

        time.sleep(0.05)
except KeyboardInterrupt:
    pass
