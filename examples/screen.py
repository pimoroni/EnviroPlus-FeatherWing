"""
The MIT License (MIT)

Copyright (c) 2019 Scott Shawcroft for Adafruit Industries LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#region Screen setup
"""
This region of code is used to setup the envirowing screen with displayio
"""

import board, time
import pimoroni_physical_feather_pins
import displayio
from adafruit_st7735r import ST7735R

spi = board.SPI() # define which spi bus the screen is on
spi.try_lock() # try to get control of the spi bus
spi.configure(baudrate=100000000) # tell the spi bus how fast it's going to run
# baudrate doesn't need to be this high in practice, it's just nice to have a quick screen refresh in this case
spi.unlock() # unlocks the spi bus so displayio can control it
tft_dc = pimoroni_physical_feather_pins.pin19() # define which pin the command line is on
tft_cs = pimoroni_physical_feather_pins.pin20() # define which pin the chip select line is on

displayio.release_displays() # release any displays that may exist from previous code run
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=pimoroni_physical_feather_pins.pin21()) # define the display bus

display = ST7735R(display_bus, width=160, height=80, colstart=26, rowstart=1, rotation=270, invert=True) # define the display (these values are specific to the envirowing's screen)

#endregion Screen setup

import terminalio
from adafruit_display_text import label

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

color_bitmap = displayio.Bitmap(160, 80, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00 # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(50, 50, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088 # Purple
inner_sprite = displayio.TileGrid(inner_bitmap,
                                  pixel_shader=inner_palette,
                                  x=10, y=10)
splash.append(inner_sprite)

# Draw a label
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=30, y=64)
splash.append(text_area)

while True:
    pass