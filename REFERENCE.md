# Reference <!-- omit in toc -->

- [Getting Started](#getting-started)
  - [Installing](#installing)
    - [Installing CircuitPython](#installing-circuitpython)
    - [Installing Adafruit Libraries](#installing-adafruit-libraries)
    - [Installing Pimoroni Libraries](#installing-pimoroni-libraries)
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

#### Installing CircuitPython

#### Installing Adafruit Libraries

#### Installing Pimoroni Libraries

#### Troubleshooting

### Examples

#### bme280-simple
[bme280-simple](..blob/master/examples/bme280-simple.py)

Prints out the readings from the temperature, pressure and humidity sensor, along with its estimated altitude calculation.

#### screen
[screen](..blob/master/examples/screen.py)

Draws a few things on the screen using displayio.

#### gas-sensor
[gas-sensor](..blob/master/examples/gas-sensor.py)

Prints the readings from the gas sensor once a second.

#### microphone
[microphone](..blob/master/examples/microphone.py)

Continuously waits for a double clap and prints when it hears one.

Perfect for hacking! Just change the code in `double_clap_function` to whatever you want; toggle an LED, show something on screen, etc.

#### particulate-sensor
[particulate-sensor](..blob/master/examples/particulate-sensor.py)

Prints the readings from the particulate sensor as fast as it supplies them (typically 1 per second).

Remember to plug it in to the header on the board!

#### proximity-and-light
[proximity-and-light](..blob/master/examples/proximity-and-light.py)

Quickly prints out the readings from the proximity and light sensor, and adjusts the screen's backlight according to the light readings.

#### plotter-bme280
[plotter-bme280](..blob/master/examples/plotter-bme280.py)

Draws a line graph of readings from the temperature, pressure and humidity sensor on the screen.

#### plotter-gas
[plotter-gas](..blob/master/examples/plotter-gas.py)

Draws a line graph of readings from the gas sensor on the screen.

#### plotter-light&sound
[plotter-light&sound](..blob/master/examples/plotter-light&sound.py)

Draws a line graph of readings from the light and proximity sensors, and the noise level determined from microphone readings on the screen.

#### plotter-particulate
[plotter-particulate](..blob/master/examples/plotter-particulate.py)

Draws a line graph of readings from the particulate sensor on the screen.

An additional red line is drawn, representing the WHO guideline, the max value that the average over 24hrs must not exceed.

Readings are scaled such that both particulates guideline values are represented by the same red line.

PM1.0 readings are disabled by default as there is no standard to compare to at this time

Remember to plug it in to the header on the board!

#### plotters-combined
[plotters-combined](..blob/master/examples/plotters-combined.py)

Combines all of the separate plotter examples into one!

You can switch page by waving your hand over the proximity sensor for a second.

If the particulate sensor isn't plugged in, it'll just skip it and still work.

#### logger-bme280
[logger-bme280](..blob/master/examples/logger-bme280.py)

TODO

#### logger-gas
[logger-gas](..blob/master/examples/logger-gas.py)

TODO

#### test-all
[test-all](..blob/master/examples/test-all.py)

Runs a full self test.

Useful for troubleshooting to see if something's wrong.

If the particulate sensor isn't plugged in, it will fail the particulate test.

#### test-all-low-mem
[test-all-low-mem](..blob/master/examples/test-all-low-mem/test-all-low-mem.py)

TODO

## Function Reference

### Sensors

#### BME280

#### Gas

#### Microphone

#### Particulate Sensor

#### Proximity and Light

### Utilities

#### Screen

#### Plotter

#### Logger

TODO