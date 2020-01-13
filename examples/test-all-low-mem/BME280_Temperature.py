def BME280_Temperature(tests, num_test_bytes, write_tests_to_nvm, reset):
    try:
        import board, adafruit_bme280
        i2c = board.I2C()
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
        bme280.sea_level_pressure = 1013.25
        if -50 <= bme280.temperature <= 50:
            tests["BME280_Temperature"]["Passed"] = True
            print("Passed with", bme280.temperature)
        else:
            tests["BME280_Temperature"]["Passed"] = False
            print("Failed")
    except Exception as e:
        tests["BME280_Temperature"]["Passed"] = False
        print("Failed with ", e)
    finally:
        tests["BME280_Temperature"]["Test Run"] = True
        write_tests_to_nvm(tests, num_test_bytes)
        reset()