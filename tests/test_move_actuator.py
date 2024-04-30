import time

import helpers.gpio as gpio


def test_expand_actuator():
    gpio.expand_actuator(10e3)
    print("Expanding actuator")
    assert True


def test_contract_actuator():
    gpio.contract_actuator(8.5e3)
    print("Contracting actuator")
    assert True


def test_angles_at_times():
    intervals = 20

    for _ in range(intervals):
        gpio.expand_actuator(10e3 / intervals)
        time.sleep(5)

    time.sleep(15)

    for _ in range(intervals):
        gpio.contract_actuator(8.5e3 / intervals)
        time.sleep(5)


if __name__ == "__main__":
    # test_expand_actuator()
    # test_contract_actuator()
    test_angles_at_times()
