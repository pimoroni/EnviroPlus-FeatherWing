def Screen(backlight_control=True, baudrate=100000000, spi=None):
    """__init__
    :param bool backlight_control: determines whether this class should handle the screen's backlight (default True)
    (this is useful to set to False if you want to control the brightness with pwm in your own code)
    :param int baudrate: sets the baudrate for the spi connection to the display (default 100000000)
    (baudrate doesn't need to be this high for the display to function, it's just nice to have a quick screen refresh by default)
    This class is used to setup the envirowing screen with displayio and return a display object
    """

    import board
    import pimoroni_physical_feather_pins
    import displayio
    from adafruit_st7735r import ST7735R

    # if not supplied an spi object, make our own
    if not spi:
        spi = board.SPI()  # define which spi bus the screen is on

    spi.try_lock()         # try to get control of the spi bus
    spi.configure(baudrate=baudrate)  # tell the spi bus how fast it's going to run
    spi.unlock()           # unlocks the spi bus so displayio can control it

    displayio.release_displays()  # release any displays that may exist from previous code run

    # define the display bus
    if backlight_control:
        display_bus = displayio.FourWire(spi, command=pimoroni_physical_feather_pins.pin19(), chip_select=pimoroni_physical_feather_pins.pin20(), reset=pimoroni_physical_feather_pins.pin21())
    else:
        display_bus = displayio.FourWire(spi, command=pimoroni_physical_feather_pins.pin19(), chip_select=pimoroni_physical_feather_pins.pin20())

    # define the display (these values are specific to the envirowing's screen)
    display = ST7735R(display_bus, width=160, height=80, colstart=26, rowstart=1, rotation=270, invert=True)

    return display
