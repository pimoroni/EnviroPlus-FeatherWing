# Reference <!-- omit in toc -->

- [Getting Started](#getting-started)
  - [Installing](#installing)
    - [Installing CircuitPython](#installing-circuitpython)
    - [Installing Adafruit CircuitPython libraries](#installing-adafruit-circuitpython-libraries)
    - [Installing Pimoroni CircuitPython libraries](#installing-pimoroni-circuitpython-libraries)
    - [Final steps](#final-steps)
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
    - [test-all](#test-all)
- [Function Reference](#function-reference)
  - [Sensors](#sensors)
    - [BME280 temperature, pressure, and humidity sensor](#bme280-temperature-pressure-and-humidity-sensor)
    - [MiCS6814 analog gas sensor](#mics6814-analog-gas-sensor)
    - [Analog microphone](#analog-microphone)
    - [PMS5003 particulate matter sensor](#pms5003-particulate-matter-sensor)
    - [LTR-559 light and proximity sensor](#ltr-559-light-and-proximity-sensor)
  - [Utilities](#utilities)
    - [Screen](#screen-1)
    - [Plotter](#plotter)

## Getting Started

### Installing

Plug your Feather board into your computer using a known-good micro-USB cable (capable of power _and_ data).

A drive called CIRCUITPY should mount on your computer. This is where the CircuitPython code and libraries live on your Feather board.

Verify that the version of CircuitPython on your Feather board is compatible with our libraries (see [Dependencies in the Readme](README.md#dependencies)).

(To check your CircuitPython version, open up the CIRCUITPY drive and check the `boot_out.txt` file)

If the version isn't compatible, follow the [Installing CircuitPython](#installing-circuitpython) step (you can skip that step if it is).

#### Installing CircuitPython

Follow [these instructions from Adafruit](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to install the correct version of Circuitpython to your board.

#### Installing Adafruit CircuitPython libraries

Follow [these instructions from Adafruit](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries) to install the correct Adafruit CircuitPython libraries to your board. If your board has limited storage space (usually non-Express Feathers), install only the libraries specified in [Dependencies](README.md#dependencies).

#### Installing Pimoroni CircuitPython libraries

Download the [latest release of CircuitPython libraries](../../releases), and copy the contents of the `lib` folder in the zip file you downloaded into the `lib` folder in your CIRCUITPY drive. Make sure you download the correct zip file; you don't want the `Source Code` one!

#### Final steps

Don't forget to attach your Enviro+ FeatherWing to your Feather! You'll need to solder headers onto it, ones that complement whatever sort of headers you have on your Feather.

To code on your Feather, you might want to use Mu. [Adafruit have instructions on how to install Mu and to set it up](https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor).

Finally, have a play! Copy an example from the zip you downloaded into the `code.py` file on CIRCUITPY, save it, and watch it work!

#### Troubleshooting

Things to check:
* Is the Enviro+ FeatherWing seated properly on the Feather?
* Is the USB cable you're using fully inserted and working? Is it capable of USB data as well as power?
* Did you check the serial output for errors?

### Examples

#### bme280-simple
[bme280_simple.py](examples/bme280_simple.py)

Prints out the readings from the BME280 temperature, pressure, and humidity sensor, along with its estimated altitude calculation.

#### screen
[screen.py](examples/screen.py)

Example of how to draw to the 0.96" LCD, using displayio.

#### gas-sensor
[gas_sensor.py](examples/gas_sensor.py)

Prints the readings from the MiCS6814 analog gas sensor once a second.

#### microphone
[microphone.py](examples/microphone.py)

Continuously waits for a double clap and prints when it hears one.

Perfect for hacking! Just change the code in `double_clap_function` to whatever you want; toggle an LED, show something on screen, etc.

#### particulate-sensor
[particulate_sensor.py](examples/particulate_sensor.py)

Prints the readings from the PMS5003 particulate matter sensor as fast as it supplies them (typically around once per second).

Remember to plug the PMS5003 particulate matter sensor into the socket on the underside of the FeatherWing!

#### proximity-and-light
[proximity_and_light.py](examples/proximity_and_light.py)

Quickly prints out the readings from the LTR-559 proximity and light sensor, and adjusts the screen's backlight according to the ambient light level readings.

#### plotter-bme280
[plotter_bme280.py](examples/plotter_bme280.py)

Draws a line graph of readings from the BME280 temperature, pressure and humidity sensor on the screen.

#### plotter-gas
[plotter_gas.py](examples/plotter_gas.py)

Draws a line graph of readings from the MiCS6814 analog gas sensor on the screen.

#### plotter-light&sound
[plotter_light_and_sound.py](examples/plotter_light_and_sound.py)

Draws a line graph of readings from the LTR-559 light and proximity sensor, and the noise level (determined from microphone readings) on the screen.

#### plotter-particulate
[plotter_particulate.py](examples/plotter_particulate.py)

Draws a line graph of readings from the PMS5003 particulate matter sensor on the screen.

An additional red line is drawn, representing the WHO's recommended maximum value that the average over 24 hours must not exceed.

Readings are scaled such that both particulate guideline values are represented by the same red line.

PM1.0 readings are not shown by default as there is no standard to compare to at this time.

Remember to plug the PMS5003 particulate matter sensor into the socket on the underside of the FeatherWing!

#### plotters-combined
[plotters_combined.py](examples/plotters_combined.py)

Combines all of the separate plotter examples into one!

You can switch page by waving your hand over the proximity sensor for one second.

If the particulate matter sensor isn't plugged in, it'll just skip it and still work.

#### test-all
[test_all.py](examples/test_all.py)

Runs a full self-test.

Useful for troubleshooting to see if something's wrong.

If the PMS5003 particulate matter sensor isn't plugged in, it will fail the particulate test.

## Function Reference

### Sensors

#### BME280 temperature, pressure, and humidity sensor

```python
import adafruit_bme280

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c_bus, address=0x76)
```
Imports and sets up the device. The address needs to be specified as we use a different default to Adafruit.

---

```python
bme280.sea_level_pressure = 1013.25
```
Sets the sea-level pressure, which is used in altitude calculation/estimation.

---

```python
print(bme280.temperature)
print(bme280.humidity)
print(bme280.pressure)
print(bme280.altitude)
```

Readings can be accessed with the above methods. Altitude, as mentioned before, is a calculation/estimation based on the other readings, and is best used as a relative reading rather than an absolute.

---

Further documentation can be found [here](https://circuitpython.readthedocs.io/projects/bme280/en/latest/)

---

#### MiCS6814 analog gas sensor

```python
from pimoroni_envirowing import gas
```

Just an import is needed here, no code setup required. However the gas sensor may need time to warm up before it gives consistent readings, a day or so from being powered, longer if this is the first time you've used it.

---

```python
print(gas.read_all())
```
This will print a well-formatted summary of all the readings.

---

```python
reading = gas.read_all()

print(reading.oxidising)
print(reading.reducing)
print(reading.nh3)
```

Individual values can be accessed by the above methods. If you attempt to access the individual readings by using, for example, `print(gas.read_all().oxidising)`, it will still work. However, if you read the other types of gas readings (reducing, NH3) in a similar fashion it will take a new reading each time, as opposed to the recommended method above which will take only one reading, and thus all the measurements will occupy the same time-slice.

---

#### Analog microphone

This one is a little different, as it doesn't have a dedicated library, and is accessed through CircuitPython's analog pin reading methods (on pin 8, in this case).

The best place to start is the [microphone example](#microphone), as CircuitPython does not yet supply a library for sampling audio quickly from raw pins.

The microphone has a DC offset of 1.5V, so it's possible to get full waveform readings from it (as Feather ADCs are usually 0-3V).

---

#### PMS5003 particulate matter sensor

```python
from pimoroni_pms5003 import PMS5003

pms5003 = PMS5003()
```
Import and setup is as above. Make sure you have the cable plugged in firmly at both ends. It'll take a little time for the sensor to start up.

---

```python
data = pms5003.read()
print(data)
```
This will print a well-formatted summary of all of the readings.

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

Individual values can be accessed by the above methods. If you attempt to access the individual readings by using, for example, `print(pms5003.read().data[0])`, it will still work, although if you make other readings in a similar fashion it will have to wait for the sensor to send a new reading each time, as opposed to the recommended method above which will use only one reading, and thus all the measurements will occupy the same time-slice.

---

#### LTR-559 light and proximity sensor

```python
from pimoroni_ltr559 import LTR559
from pimoroni_circuitpython_adapter import not_SMBus

i2c_dev = not_SMBus()
ltr559 = LTR559(i2c_dev=i2c_dev)
```
Import and setup is as above. `not_SMBus` is needed, as CircuitPython does not natively expose the I2C functions that the library expects and requires.

---

```python
lux = ltr559.get_lux()
prox = ltr559.get_proximity()
print(lux)
print(prox)
```

---

Light and proximity readings can be obtained using the above methods.

Interrupts can be set up similarly to [the proximity interrupt example in the library](https://github.com/pimoroni/ltr559-python/blob/master/examples/proximity-interrupt.py), however CircuitPython does not yet have a function for native interrupts at the time of writing.

The LTR-559 interrupt pin is broken out to pin 24 on the Enviro+ FeatherWing.

---

### Utilities

#### Screen

```python
from pimoroni_envirowing import screen

display = screen.Screen()
```

The above will import, setup, and initialise the display on the Enviro+ FeatherWing. If you're using another device on the SPI bus, you'll need to use the `spi` option to pass it the shared SPI bus.

If you want to control the backlight, you'll first need to use the `backlight_control=False` option, and then send a PWM signal out to pin 21, as seen in [the proximity-and-light example](#proximity-and-light).

You can then go on to use the `display` object with `displayio`.

#### Plotter

```python
from pimoroni_envirowing.screen import plotter

white = 0xFFFFFF

splotter = plotter.ScreenPlotter([white])
```

The most simple import and setup of plotter is as above. This will allow you to plot one reading over time, drawn in white, with the default min. and max. values, which match those of CircuitPython's raw analog input readings (0 to 65535).

Here's an example of that:

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

To add more readings, more colours need to be added to the list in the plotter setup, e.g.:

```python
white = 0xFFFFFF
red = 0xFF0000
splotter = plotter.ScreenPlotter([white, red])
```

You can then add more values to the update call:

```python
    splotter.update(analog_in.value, another_analog_in.value)
```

These will be coloured in the same order you define the colours in the setup. So `analog_in` will be white, and `another_analog_in` will be red.

The number of colours you define in setup must be equal to, or more than, the number of readings you make in `update`.

More advanced usage can be found in [the plotter examples](#plotter-bme280), and [the plotter code itself](library/pimoroni_envirowing/screen/plotter.py).
