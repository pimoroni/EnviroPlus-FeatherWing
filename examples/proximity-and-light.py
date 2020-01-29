import time
import pulseio
from pimoroni_ltr559 import LTR559
from pimoroni_circuitpython_adapter import not_SMBus
import pimoroni_physical_feather_pins
from pimoroni_envirowing import screen

screen = screen.Screen(backlight_control=False)

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
        pwm.duty_cycle = int(min(remap(lux, 0, 400, 3, (2**16 - 1)), (2**16 - 1)))

        print("Lux: {:06.2f}, Proximity: {:04d}".format(lux, prox))

        time.sleep(0.05)
except KeyboardInterrupt:
    pass
