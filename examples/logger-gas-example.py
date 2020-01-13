from pimoroni_envirowing import gas
from pimoroni_envirowing.screen import logger

import time

# colours for the logger are defined as rgb values in hex, with 2 bytes for each colour
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF

# the max value is set to 5 as the gas library outputs values in volts, up to a max of 5
slogger = logger.ScreenLogger([red, green, blue], max_value=5, min_value=0)

while True:
    #take readings
    reading = gas.read_all()

    # update the line graph
    slogger.update(
        reading.oxidising,
        reading.reducing,
        reading.nh3
    )
    
    time.sleep(0.1)