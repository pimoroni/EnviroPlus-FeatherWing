# Enviro+ FeatherWing

[Buy Enviro+ FeatherWing here.](https://shop.pimoroni.com/enviro-plus-featherwing)

Care about air with Enviro+ FeatherWing. It's packed full of environmental sensors that'll get you started in the world of citizen science. Monitor weather, light level, noise pollution, and air quality, in your local area and contribute your data to better understand trends in air pollution.

## Quick start
If you know what you're doing, follow the instructions below.

If you need a bit more detail, then follow our detailed [Getting Started](../../blob/master/REFERENCE.md) guide

### Recommended hardware

We recommend using the following hardware:
* [Adafruit Feather M4 Express](https://shop.pimoroni.com/products/adafruit-feather-m4-express-featuring-atsamd51-atsamd51-cortex-m4)
* [PMS5003 Particulate Matter Sensor with Cable](https://shop.pimoroni.com/products/pms5003-particulate-matter-sensor-with-cable)
* Optional:
  * [LiPo battery](https://shop.pimoroni.com/products/lipo-battery-pack) if you want to use it portably without a usb power bank
  * [USB-A to micro-B cable](https://shop.pimoroni.com/products/usb-a-to-microb-cable-black) if you don't have a spare one, or you want more!

### Recommended software

We recommend using [Mu editor](https://codewith.mu/), as it has built-in support for CircuitPython devices.


### Dependencies

* [CircuitPython 4.x](https://circuitpython.org/downloads) (soon to be 5.x)
* [Adafruit CircuitPython Library Bundle](https://circuitpython.org/libraries)
    * Specifically `adafruit_st7735r`, `adafruit_bme280`, `adafruit_bus_device`
    * Optionally `adafruit_display_text` (needed for the screen and the BME280 logging examples, and if you want to display text on the screen)
* [The latest release of the Enviro+ FeatherWing libraries (this repository!)](../../releases)

## Warning
The following examples will not work on the M0 boards, due to their limited RAM compared to other CircuitPython Feather boards:
* `plotter-bme280.py`
* `test-all.py`

## Development
To clone the repository, please use `git clone` with the option `--recurse-submodules`, otherwise not all the libraries will be downloaded. Do not download the zip as this will not contain all the libraries either.

Example: `git clone https://github.com/pimoroni/EnviroPlus-FeatherWing --recurse-submodules`

When cloning, the symlinks set up for library building only seem to work on Linux. You may also need to make sure this config option hasn't been set to False: `git config --get core.symlinks`
