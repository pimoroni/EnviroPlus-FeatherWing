from microcontroller import nvm, reset

tests = {
    "Screen":
        {"Test Run":False, "Passed":False},
    "I2C":
        {"Test Run":False, "Passed":False},
    "BME280_Temperature":
        {"Test Run":False, "Passed":False},
    "BME280_Humidity":
        {"Test Run":False, "Passed":False},
    "BME280_Pressure":
        {"Test Run":False, "Passed":False},
    "Gas_Oxidising":
        {"Test Run":False, "Passed":False},
    "Gas_Reducing":
        {"Test Run":False, "Passed":False},
    "Gas_NH3":
        {"Test Run":False, "Passed":False},
    "Light":
        {"Test Run":False, "Passed":False},
    "Prox":
        {"Test Run":False, "Passed":False},
    "Mic":
        {"Test Run":False, "Passed":False},
    "PMS5003":
        {"Test Run":False, "Passed":False},
    "Finished": False,
    "Read": False
    }

def restart_tests(num_test_bytes):
    nvm[0:num_test_bytes] = bytearray(num_test_bytes)
    reset()

def read_tests_from_nvm(bool_bytes, tests):
    keys = list(tests.keys())
    keys.sort()
    i = 0
    for test in keys:
        if test not in ("Finished", "Read"):
            tests[test]["Test Run"] = int(bool_bytes[i])
            i += 1
            tests[test]["Passed"] = int(bool_bytes[i])
            i += 1
        else:
            tests[test] = int(bool_bytes[i])
            i +=1
    return tests

def write_tests_to_nvm(tests, num_test_bytes):
    bits = [0]*num_test_bytes
    keys = list(tests.keys())
    keys.sort()
    i = 1
    for test in keys:
        if test not in ("Finished", "Read"):
            bits[i] = nvm[i] = int(tests[test]["Test Run"])
            i += 1
            bits[i] = nvm[i] = int(tests[test]["Passed"])
            i += 1
        else:
            bits[i] = nvm[i] = int(tests[test])
            i += 1
    nvm[0] = sum(bits) # checksum

def check_if_finished(tests):
    finished = True
    for test in tests.keys():
        if test not in ("Finished", "Read"):
            if not tests[test]["Test Run"]:
                    finished = False
    tests["Finished"] = finished
    return tests

def display_results(tests):
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

    failed = []
    for test in tests.keys():
        if test not in ("Finished", "Read"):
            if not tests[test]["Passed"]:
                failed.append(test)
    
    if not failed:
        print("All Tests Passed!")
    else:
        print("These tests failed:")
        print(", ".join(failed))
    tests["Read"] = True
    write_tests_to_nvm(tests, num_test_bytes)
    while True:
        pass
    #reset()

num_test_bytes = (len(tuple(tests.keys())) * 2 - 1) # -2, +1, because 2 tests don't have Run and Passed properties, but 1 byte is used for the checksum

nvm_checksum = nvm[0]

bool_bytes = nvm[1:num_test_bytes]

calc_checksum = sum(bool_bytes)

if nvm_checksum != calc_checksum:
    print(nvm_checksum, " != ", calc_checksum)
    print("Checksum Mismatch")
    restart_tests(num_test_bytes)
else:
    tests = read_tests_from_nvm(bool_bytes, tests)
    print("Read tests from NVM")
    tests = check_if_finished(tests)
    print("Checked if tests are finished")
    if tests["Read"]:
        print("Tests finished and read. Resetting...")
        restart_tests(num_test_bytes)
    elif tests["Finished"]:
        print("Tests finished. Displaying...")
        display_results(tests)
    else:
        for test in tests.keys():
            if test not in ("Finished", "Read"):
                if not tests[test]["Test Run"]:
                    print("Running", test)
                    importedtest = __import__(test, globals(), locals(), [None], 1)
                    getattr(importedtest, test)(tests, num_test_bytes, write_tests_to_nvm, reset)
