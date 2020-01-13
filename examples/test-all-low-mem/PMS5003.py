def PMS5003(tests, num_test_bytes, write_tests_to_nvm, reset):
    try:
        from pimoroni_pms5003 import PMS5003
        pms5003 = PMS5003()
        if pms5003.read():
            tests["PMS5003"]["Passed"] = True
            print("Passed with", pms5003.read())
        else:
            tests["PMS5003"]["Passed"] = False
            print("Failed")
    except Exception as e:
        tests["PMS5003"]["Passed"] = False
        print("Failed with ", e)
    finally:
        tests["PMS5003"]["Test Run"] = True
        write_tests_to_nvm(tests, num_test_bytes)
        reset()