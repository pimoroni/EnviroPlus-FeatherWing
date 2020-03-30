# Reference <!-- omit in toc -->

- [Getting Started](#getting-started)
  - [Installing](#installing)
    - [Installing CircuitPython](#installing-circuitpython)
    - [Installing Adafruit Libraries](#installing-adafruit-libraries)
    - [Installing Pimoroni Libraries](#installing-pimoroni-libraries)
    - [Finally](#finally)
    - [Troubleshooting](#troubleshooting)
  - [Examples](#examples)
    - [bme280-simple](#bme280-simple)
    - [screen](#screen)
    - [gas-sensor](#gas-sensor)
    - [microphone](#microphone)
    - [particulate-sensor](#particulate-sensor)
    - [proximity-and-light](#proximity-and-light)
    - [plotter-bme280](#plotter-bme280)
    - [plotter-gas](#plotter-gas)
    - [plotter-light&sound](#plotter-lightsound)
    - [plotter-particulate](#plotter-particulate)
    - [plotters-combined](#plotters-combined)
    - [logger-bme280](#logger-bme280)
    - [logger-gas](#logger-gas)
    - [test-all](#test-all)
    - [test-all-low-mem](#test-all-low-mem)
- [Function Reference](#function-reference)
  - [Sensors](#sensors)
    - [BME280](#bme280)
    - [Gas](#gas)
    - [Microphone](#microphone-1)
    - [Particulate Sensor](#particulate-sensor-1)
    - [Proximity and Light](#proximity-and-light-1)
  - [Utilities](#utilities)
    - [Screen](#screen-1)
    - [Plotter](#plotter)
    - [Logger](#logger)

## Getting Started

### Installing

Plug in your Feather board to your computer using a known good micro usb data cable.

Verify that the version of circuitpython on the board is a compatible one with our libraries (see [Dependencies in the Readme](../../blob/master/README.md#dependencies)).

(To find this out, open up the CIRCUITPY drive and read the `boot_out.txt` file)

If it's not, follow the [Installing CircuitPython](#installing-circuitpython) step (you can skip that step if it is).

#### Installing CircuitPython

Follow [these instructions from Adafruit](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to install the correct version of circuitpython to your board.

#### Installing Adafruit Libraries

Follow [these instructions from Adafruit](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries) to install the correct Adafruit libraries to your board.
If your board has limited storage space (usually non-Express Feathers), install only the libraries specified in [Dependencies](../../blob/master/README.md#dependencies).

#### Installing Pimoroni Libraries

Download the [latest release](../../releases), and copy the contents of the `lib` folder in the zip you downloaded into the `lib` folder in your CIRCUITPY drive. Make sure you download the correct zip, you don't want the `Source Code` one!

#### Finally

Don't forget to attach your EnviroWing to your Feather!

To code on your feather, you might want to use Mu. [Adafruit have instructions on how to install it and set it up](https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor).

Finally, have a play! Copy an example from the zip you downloaded into `code.py` on CIRCUITPY, and watch it work!

#### Troubleshooting

Things to check:
* Is the EnviroWing seated properly on the Feather?
* Is the usb cable you're using fully inserted and working?
* Did you check the serial output for errors?

### Examples

#### bme280-simple
[bme280-simple.py](../../blob/master/examples/bme280-simple.py)

Prints out the readings from the temperature, pressure and humidity sensor, along with its estimated altitude calculation.

#### screen
[screen.py](../../blob/master/examples/screen.py)

Draws a few things on the screen using displayio.

#### gas-sensor
[gas-sensor.py](../../blob/master/examples/gas-sensor.py)

Prints the readings from the gas sensor once a second.

#### microphone
[microphone.py](../../blob/master/examples/microphone.py)

Continuously waits for a double clap and prints when it hears one.

Perfect for hacking! Just change the code in `double_clap_function` to whatever you want; toggle an LED, show something on screen, etc.

#### particulate-sensor
[particulate-sensor.py](../../blob/master/examples/particulate-sensor.py)

Prints the readings from the particulate sensor as fast as it supplies them (typically 1 per second).

Remember to plug it in to the header on the board!

#### proximity-and-light
[proximity-and-light.py](../../blob/master/examples/proximity-and-light.py)

Quickly prints out the readings from the proximity and light sensor, and adjusts the screen's backlight according to the light readings.

#### plotter-bme280
[plotter-bme280.py](../../blob/master/examples/plotter-bme280.py)

Draws a line graph of readings from the temperature, pressure and humidity sensor on the screen.

#### plotter-gas
[plotter-gas.py](../../blob/master/examples/plotter-gas.py)

Draws a line graph of readings from the gas sensor on the screen.

#### plotter-light&sound
[plotter-light&sound.py](../../blob/master/examples/plotter-light&sound.py)

Draws a line graph of readings from the light and proximity sensors, and the noise level determined from microphone readings on the screen.

#### plotter-particulate
[plotter-particulate.py](../../blob/master/examples/plotter-particulate.py)

Draws a line graph of readings from the particulate sensor on the screen.

An additional red line is drawn, representing the WHO guideline, the max value that the average over 24hrs must not exceed.

Readings are scaled such that both particulates guideline values are represented by the same red line.

PM1.0 readings are disabled by default as there is no standard to compare to at this time

Remember to plug it in to the header on the board!

#### plotters-combined
[plotters-combined.py](../../blob/master/examples/plotters-combined.py)

Combines all of the separate plotter examples into one!

You can switch page by waving your hand over the proximity sensor for a second.

If the particulate sensor isn't plugged in, it'll just skip it and still work.

#### logger-bme280
[logger-bme280.py](../../blob/master/examples/logger-bme280.py)

TODO

#### logger-gas
[logger-gas.py](../../blob/master/examples/logger-gas.py)

TODO

#### test-all
[test-all.py](../../blob/master/examples/test-all.py)

Runs a full self test.

Useful for troubleshooting to see if something's wrong.

If the particulate sensor isn't plugged in, it will fail the particulate test.

#### test-all-low-mem
[test-all-low-mem.py](../../blob/master/examples/test-all-low-mem/test-all-low-mem.py)

TODO

## Function Reference

### Sensors

#### BME280

```python
import adafruit_bme280

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c_bus, address=0x76)
```
Imports and sets up the device, the address needs to be specified as we use a different default to adafruit.

---

```python
bme280.sea_level_pressure = 1013.25
```
Sets the sea level pressure, which is used in altitude calculation/estimation

---

```python
print(bme280.temperature)
print(bme280.humidity)
print(bme280.pressure)
print(bme280.altitude)
```
Readings can be accessed with the above methods, Altitude as mentioned before is a calculation/estimation based off the other readings,and is best used as a relative reading rather than an absolute.

---

Further documentation can be found [here](https://circuitpython.readthedocs.io/projects/bme280/en/latest/)

---

#### Gas

```python
from pimoroni_envirowing import gas
```
Just an import is needed here, no code setup required. However the gas sensor may need time to warm up before it gives consistent readings, a day or so from being powered, longer if this is the first time you've used it.

---

```python
print(gas.read_all())
```
This will print a well formatted summary of all the readings.

---

```python
reading = gas.read_all()

print(reading.oxidising)
print(reading.reducing)
print(reading.nh3)
```
Individual values can be accessed by the above methods. If you attempt to access the individual readings by using for example `print(gas.read_all().oxidising)`, it will still work, however if you make other readings in a similar fashion it will make a new reading each time, as opposed to the recommended method above which will make only one reading, and thus all the measurements will occupy the same time slice.

---

#### Microphone

This one is a little different, as it doesn't have a dedicated library, and is accessed through circuitpython's analogue pin reading methods.

The best place to start is the [microphone example](#microphone), as circuitpython does not yet supply a library for sampling audio quickly from raw pins.

TODO: mention which pin the mic is on

The microphone has a DC offset of 1.5V, so it's possible to get full waveform readings from it (as feather ADCs are usually 0-3V)

---

#### Particulate Sensor

```python
from pimoroni_pms5003 import PMS5003

pms5003 = PMS5003()
```
Import and setup is as above, make sure you have the cable plugged firmly in at both ends. It'll take a little time for the sensor to start up, within a minute or so.

---

```python
data = pms5003.read()
print(data)
```
This will print a well formatted summary of all the readings.

The sensor typically send new readings every second.

---

```python
reading = pms5003.read()
pm1 = reading.data[0] # PM1.0
pm2 = reading.data[1] # PM2.5
pm10 = reading.data[2] # PM10
print(pm1)
print(pm2)
print(pm10)
```
Individual values can be accessed by the above methods. If you attempt to access the individual readings by using for example `print(pms5003.read().data[0])`, it will still work, however if you make other readings in a similar fashion it will have to wait for the sensor to send a new reading each time, as opposed to the recommended method above which will use only one reading, and thus all the measurements will occupy the same time slice.

---

#### Proximity and Light

```python
from pimoroni_ltr559 import LTR559
from pimoroni_circuitpython_adapter import not_SMBus

i2c_dev = not_SMBus()
ltr559 = LTR559(i2c_dev=i2c_dev)
```
Import and setup is as above. `not_SMBus` is needed as circuitpython does not natively expose the i2c functions that the library expects and requires.

---

```python
lux = ltr559.get_lux()
prox = ltr559.get_proximity()
print(lux)
print(prox)
```
Light and proximity reading can be obtained using the above methods.

---

Interrupts can be set up similarly to [the proximity interrupt example in the library](https://github.com/pimoroni/ltr559-python/blob/master/examples/proximity-interrupt.py), however circuitpython does not yet have a function for native interrupts at the time of writing.

The LTR-559 interrupt pin is broken out to Pin 24 on the wing.

---

### Utilities

#### Screen

```python
from pimoroni_envirowing import screen

display = screen.Screen()
```
The above will import, setup and initialise the display on the envirowing. If you're using another device on the SPI bus, you'll want to use the `spi` option to pass it the shared SPI bus.

If you want to control the backlight, you'll first need to use the `backlight_control=False` option, and then send a pwm signal out to Pin 21, as seen in [the proximity-and-light example](#proximity-and-light).

You can then go on to use the `display` object with displayio.

#### Plotter

```python
from pimoroni_envirowing.screen import plotter

white = 0xFFFFFF

splotter = plotter.ScreenPlotter([white])
```
The most simple import and setup of plotter is as above.
This will allow you to plot one reading over time, drawn in white, with the default min and max values, which match those of circuitpython's raw analogue input readings (0 to 65535).

An example of so, updating once a second, follows:

```python
import time
import board
from analogio import AnalogIn
from pimoroni_envirowing.screen import plotter

analog_in = AnalogIn(board.A1)

white = 0xFFFFFF

splotter = plotter.ScreenPlotter([white])

while True:
    splotter.update(analog_in.value)
    time.sleep(1)
```

To add more readings, more colours need to be added to the list in the plotter setup, eg:
```python
white = 0xFFFFFF
red = 0xFF0000
splotter = plotter.ScreenPlotter([white, red])
```
You then simply add more values to the update call:
```python
    splotter.update(analog_in.value, another_analog_in.value)
```
These will be coloured in the same order you define the colours in the setup. So `analog_in` will be white, and `another_analog_in` will be red.

The number of colours you define in setup must be equal to or more than the number of readings you make in `update`.

More advanced usage can be found in [the plotter examples](#plotter-bme280), and [the plotter code itself](../../blob/master/library/pimoroni_envirowing/screen/plotter.py).

#### Logger

TODO