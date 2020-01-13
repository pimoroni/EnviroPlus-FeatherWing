def Gas_Reducing(tests, num_test_bytes, write_tests_to_nvm, reset):
    try:
        from pimoroni_envirowing import gas
        if 0 <= gas.read_all().reducing <= 5:
            tests["Gas_Reducing"]["Passed"] = True
            print("Passed with", gas.read_all().reducing)
        else:
            tests["Gas_Reducing"]["Passed"] = False
            print("Failed")
    except Exception as e:
        tests["Gas_Reducing"]["Passed"] = False
        print("Failed with ", e)
    finally:
        tests["Gas_Reducing"]["Test Run"] = True
        write_tests_to_nvm(tests, num_test_bytes)
        reset()