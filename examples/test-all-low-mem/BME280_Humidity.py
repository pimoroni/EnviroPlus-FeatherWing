def BME280_Humidity(tests, num_test_bytes, write_tests_to_nvm, reset):
    try:
        import board, adafruit_bme280
        i2c = board.I2C()
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
        bme280.sea_level_pressure = 1013.25
        if 0 <= bme280.humidity <= 100:
            tests["BME280_Humidity"]["Passed"] = True
            print("Passed with", bme280.humidity)
        else:
            tests["BME280_Humidity"]["Passed"] = False
            print("Failed")
    except Exception as e:
        tests["BME280_Humidity"]["Passed"] = False
        print("Failed with ", e)
    finally:
        tests["BME280_Humidity"]["Test Run"] = True
        write_tests_to_nvm(tests, num_test_bytes)
        reset()