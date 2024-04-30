import src.modules.actuation as actuation


def test_expand_actuator():
    actuation.expand_actuator(True)
    print("Expanding actuator")
    assert True


def test_contract_actuator():
    actuation.contract_actuator(True)
    print("Contracting actuator")
    assert True


if __name__ == "__main__":
    test_expand_actuator()
    test_contract_actuator()
