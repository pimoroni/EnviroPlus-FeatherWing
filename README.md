# Enviro Plus FeatherWing

## Quick Start
If you know what you're doing, start here:

If not, follow our detailed [Getting Started](..blob/master/REFERENCE.md) guide

### Recommended Hardware

We recommend using the following hardware:
* [Adafruit Feather M4 Express](https://shop.pimoroni.com/products/adafruit-feather-m4-express-featuring-atsamd51-atsamd51-cortex-m4)
* [PMS5003 Particulate Matter Sensor with Cable](https://shop.pimoroni.com/products/pms5003-particulate-matter-sensor-with-cable)
* Optional:
  * [Lipoly battery](https://shop.pimoroni.com/products/lipo-battery-pack) if you want to use it portably without a usb power bank
  * [USB A to microB cable](https://shop.pimoroni.com/products/usb-a-to-microb-cable-black) if you don't have a spare one, or you want more!

### Recommended Software

We recommend using [Mu editor](https://codewith.mu/), as it has built in support for circuitpython devices


## Requirements

* [Circuitpython 4.x](https://circuitpython.org/downloads) (soon to be 5.x)
* [Adafruit CircuitPython Library Bundle](https://circuitpython.org/libraries)
    * Specifically `adafruit_st7735r`, `adafruit_bme280`, `adafruit_bus_device`
    * Optionally `adafruit_display_text` (needed for the screen and the bm280 logging examples, and if you want to display text on the screen)

## Warning
The following examples will not work on the M0 boards, this is due to their limited RAM compared to other circuitpython feather boards:
* `plotter-bme280.py`
* 
* `test-all.py`

## Development
To clone the repository, please use `git clone` with the option `--recurse-submodules`, otherwise not all the libraries will be downloaded. Do not download the zip as this will not contain all the libraries either.

Example: `git clone https://github.com/pimoroni/EnviroPlus-FeatherWing --recurse-submodules`
