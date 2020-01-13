## Requirements

* [Circuitpython 4.x](https://circuitpython.org/downloads)
* [Adafruit CircuitPython Library Bundle](https://circuitpython.org/libraries)
    * Specifically `adafruit_st7735r`, `adafruit_bme280`, `adafruit_bus_device`
    * Optionally `adafruit_display_text` (needed for the screen and the bm280 logging examples, and if you want to display text on the screen)

## Warning
The following examples will not work on the M0 boards, this is due to their limited RAM compared to other circuitpython feathers:
* `logger-bme280-example.py`
* 
* `test-all.py`