import src.helpers.gpio as gpio


def test_expand_actuator():
    gpio.expand_actuator(True)
    print("Expanding actuator")
    assert True


def test_contract_actuator():
    gpio.contract_actuator(True)
    print("Contracting actuator")
    assert True


if __name__ == "__main__":
    test_expand_actuator()
    test_contract_actuator()
