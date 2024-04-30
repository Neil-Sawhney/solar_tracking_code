import time

import src.helpers.gpio as gpio


def test_fatigue():
    num_of_tests = 500
    for _ in range(num_of_tests):
        gpio.expand_actuator(10e3)
        time.sleep(5)
        gpio.contract_actuator(8.5e3)
        time.sleep(5)
    assert True
