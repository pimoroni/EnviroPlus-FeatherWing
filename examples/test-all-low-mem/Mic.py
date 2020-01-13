def Mic(tests, num_test_bytes, write_tests_to_nvm, reset):
    try:
        import analogio, pimoroni_physical_feather_pins, time
        mic = analogio.AnalogIn(pimoroni_physical_feather_pins.pin8())
        samples = list(range(20))
        clap_time = 0
        half_second = 500000000 # measured in nanoseconds
        clap_threshold = 1000 # the higher the value the less sensitive
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
        print("Please Double Clap. If nothing happens, there may be a problem with the Mic")
        while True: # detection start
            for i in range(20): # take 20 samples of how loud it is
                samples[i] = abs(mic.value - 32768)

            if (sum(samples)/20) > clap_threshold: # if clap found

                if not clap_time + half_second >= time.monotonic_ns(): # if another clap hasn't happened in the last half second
                    #print("Clap at {}".format(time.monotonic_ns()))
                    clap_time = time.monotonic_ns() # update the last time a clap happened
                    time.sleep(0.1)
                else: # if another clap has happened in the last half second
                    print("Double Clap Detected!")
                    break
        tests["Mic"]["Passed"] = True
    except Exception as e:
        tests["Mic"]["Passed"] = False
        print("Failed with ", e)
    finally:
        tests["Mic"]["Test Run"] = True
        write_tests_to_nvm(tests, num_test_bytes)
        reset()