def Gas_Oxidising(tests, num_test_bytes, write_tests_to_nvm, reset):
    try:
        from pimoroni_envirowing import gas
        if 0 <= gas.read_all().oxidising <= 5:
            tests["Gas_Oxidising"]["Passed"] = True
            print("Passed with", gas.read_all().oxidising)
        else:
            tests["Gas_Oxidising"]["Passed"] = False
            print("Failed")
    except Exception as e:
        tests["Gas_Oxidising"]["Passed"] = False
        print("Failed with ", e)
    finally:
        tests["Gas_Oxidising"]["Test Run"] = True
        write_tests_to_nvm(tests, num_test_bytes)
        reset()