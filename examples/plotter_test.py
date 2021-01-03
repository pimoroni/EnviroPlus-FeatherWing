"""
plotter_test.py

This only tests some aspects of the plotter object.
It does not display any data from the Enviro+ FeatherWing.
"""


import time
import gc

import pulseio
import terminalio
from adafruit_display_text import label

import pimoroni_physical_feather_pins
from pimoroni_envirowing import screen
from pimoroni_envirowing.screen import plotter


# Setup screen - this returns an ST7735R object
screen = screen.Screen(backlight_control=False)

# PWM for screen brightness
backlight_pwm = pulseio.PWMOut(pimoroni_physical_feather_pins.pin21())
backlight_pwm.duty_cycle = 65535  # full brightness

red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF


def timeit(func):
    after = 0
    before = time.monotonic_ns()
    func()
    after = time.monotonic_ns()
    return (after - before) / 1e9


def test_fourlines(name, full_refresh=False):
    test_splotter = plotter.ScreenPlotter([red, green, blue, red+green+blue],
                                          min_value=0, max_value=100, top_space=10+10,
                                          display=screen)

    # add a colour coded text label for each reading
    test_splotter.group.append(label.Label(terminalio.FONT,
                                           text="A: {:.0f}",
                                           color=red, x=0, y=5, max_glyphs=15))
    test_splotter.group.append(label.Label(terminalio.FONT,
                                           text="B: {:.0f}",
                                           color=green, x=50, y=5, max_glyphs=15))
    test_splotter.group.append(label.Label(terminalio.FONT,
                                           text="C: {:.0f}",
                                           color=blue, x=110, y=5, max_glyphs=15))
    test_splotter.group.append(label.Label(terminalio.FONT,
                                           text=name + (" CLS" if full_refresh else ""),
                                           color=0xffffff, x=0, y=5))

    for idx in range(200):
        time.sleep(0.050)
        test_splotter.update((idx * 2 + 50) % 121,
                             (idx * 2 + 20) % 101,
                             idx * 4 % 101,
                             50,
                             draw=not full_refresh)
        if full_refresh:
            test_splotter.draw(full_refresh=full_refresh)


def test_threeflatlines(name, full_refresh=False):
    test_splotter = plotter.ScreenPlotter([red, green, blue],
                                          min_value=0, max_value=100, top_space=10,
                                          display=screen)

    test_splotter.group.append(label.Label(terminalio.FONT,
                                           text=name + (" CLS" if full_refresh else ""),
                                           color=0xffffff, x=0, y=5))

    for _ in range(200):
        time.sleep(0.050)
        test_splotter.update(0,
                             50,
                             100,
                             draw=not full_refresh)

        if full_refresh:
            test_splotter.draw(full_refresh=full_refresh)


def test_twolinesfewdraws(name, full_refresh=False):
    """Only issue a draw every 4 updates to see how library handles it.
       Current implementation (Dec-2020) misses pixels until it starts scrolling.
    """
    test_splotter = plotter.ScreenPlotter([red+green, green+blue],
                                          min_value=0, max_value=1000, top_space=10+10,
                                          display=screen)

    test_splotter.group.append(label.Label(terminalio.FONT,
                                           text=name + (" CLS" if full_refresh else ""),
                                           color=0xffffff, x=0, y=5))

    for idx in range(200):
        time.sleep(0.050)
        test_splotter.update((idx * 50 + 20) % 1001,
                             (idx * 2 + 300) % 1001,
                             draw=False)
        if idx % 4 == 0:
            test_splotter.draw(full_refresh=full_refresh)


# full_refresh is currently (Dec-2020) very slow and very flickery unless
# data update rate is very low
screen_name = "Four lines, 3 ramping"
print(screen_name, "took",
      timeit(lambda: test_fourlines(screen_name)),
      "seconds")
time.sleep(10)
print(screen_name, "took",
      timeit(lambda: test_fourlines(screen_name, full_refresh=True)),
      "seconds")
time.sleep(15)

screen_name = "Three flat lines"
print(screen_name, "took",
      timeit(lambda: test_threeflatlines(screen_name)),
      "seconds")
time.sleep(10)
print(screen_name, "took",
      timeit(lambda: test_threeflatlines(screen_name, full_refresh=True)),
      "seconds")
time.sleep(15)


screen_name = "Two lines, few draws"
print(screen_name, "took",
      timeit(lambda: test_twolinesfewdraws(screen_name)),
      "seconds")
time.sleep(10)
print(screen_name, "took",
      timeit(lambda: test_twolinesfewdraws(screen_name, full_refresh=True)),
      "seconds")
time.sleep(15)
