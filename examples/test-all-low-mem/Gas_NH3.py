def Gas_NH3(tests, num_test_bytes, write_tests_to_nvm, reset):
    try:
        from pimoroni_envirowing import gas
        if 0 <= gas.read_all().nh3 <= 5:
            tests["Gas_NH3"]["Passed"] = True
            print("Passed with", gas.read_all().nh3)
        else:
            tests["Gas_NH3"]["Passed"] = False
            print("Failed")
    except Exception as e:
        tests["Gas_NH3"]["Passed"] = False
        print("Failed with ", e)
    finally:
        tests["Gas_NH3"]["Test Run"] = True
        write_tests_to_nvm(tests, num_test_bytes)
        reset()