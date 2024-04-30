import time

import src.helpers.gpio as gpio


def test_expand_actuator():
    gpio.expand_actuator(10e3)
    print("Expanding actuator")
    assert True


def test_contract_actuator():
    gpio.contract_actuator(8.5e3)
    print("Contracting actuator")
    assert True


if __name__ == "__main__":
    test_expand_actuator()
    test_contract_actuator()
