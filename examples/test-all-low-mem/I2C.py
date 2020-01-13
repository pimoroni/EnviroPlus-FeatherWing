def I2C(tests, num_test_bytes, write_tests_to_nvm, reset):
    try:
        import board
        i2c = board.I2C()
        if i2c:
            tests["I2C"]["Passed"] = True
            print("Passed with", i2c)
        else:
            tests["I2C"]["Passed"] = False
            print("Failed")
    except Exception as e:
        tests["I2C"]["Passed"] = False
        print("Failed with ", e)
    finally:
        tests["I2C"]["Test Run"] = True
        write_tests_to_nvm(tests, num_test_bytes)
        reset()