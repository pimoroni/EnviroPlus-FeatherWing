from pimoroni_envirowing import gas
import time
while True:
    try:
        print(gas.read_all())
        time.sleep(0.1)
    finally:
        gas.cleanup()