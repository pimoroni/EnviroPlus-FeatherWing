def Screen(tests, num_test_bytes, write_tests_to_nvm, reset):
    try:
        import board, pimoroni_physical_feather_pins, displayio
        from adafruit_st7735r import ST7735R
        #region Screen setup
        """
        This region of code is used to setup the envirowing screen with displayio
        """

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
        if display:
            tests["Screen"]["Passed"] = True
            print("Passed with", display)
        else:
            tests["Screen"]["Passed"] = False
            print("Failed")
    except Exception as e:
        tests["Screen"]["Passed"] = False
        print("Failed with ", e)
    finally:
        tests["Screen"]["Test Run"] = True
        write_tests_to_nvm(tests, num_test_bytes)
        reset()