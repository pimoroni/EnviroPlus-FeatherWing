from pimoroni_pms5003 import PMS5003

print("""particulate-sensor.py - Continuously print all data values.

Press Ctrl+C to exit!

""")

pms5003 = PMS5003()

try:
    while True:
        data = pms5003.read()
        print(data)

except KeyboardInterrupt:
    pass