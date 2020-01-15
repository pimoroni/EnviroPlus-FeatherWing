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

## Downloading
To clone the repository, please use `git clone` with the option `--recurse-submodules`, otherwise not all the libraries will be downloaded. Do not download the zip as this will not contain all the libraries either.

Example: `git clone https://github.com/pimoroni/EnviroPlus-FeatherWing --recurse-submodules`
