import time

import src.helpers.gpio as gpio
import src.helpers.hardware_config as h_cfg
import src.modules.actuation as actuation

def test_contraction_consistency():
    # Test the consistency of the desired angle by going repeatedly from max_expansion_angle to every angle in between to max_compression_angle in 1 degree increments
    num_of_tests = 100
    for _ in range(num_of_tests):
        for angle in range(h_cfg.max_expansion_angle, h_cfg.max_compression_angle, 1):
            # contract the actuator to the desired angle
            gpio.contract_actuator(actuation.actuation_time_to_get_to_angle(angle, False))

            # home the actuator
            time.sleep(0.1)
            gpio.contract_actuator(actuation.actuation_time_to_get_to_angle(h_cfg.max_expansion_angle) + 1000, True)
            time.sleep(0.1)
    assert True


def test_expansion_consistency():
    # Test the consistency of the desired angle by going repeatedly from max_compression_angle to every angle in between to max_expansion_angle in 1 degree increments
    num_of_tests = 100
    for _ in range(num_of_tests):
        for angle in range(h_cfg.max_compression_angle, h_cfg.max_expansion_angle, 1):
            # expand the actuator to the desired angle
            gpio.expand_actuator(actuation.actuation_time_to_get_to_angle(angle, True))

            # home the actuator
            time.sleep(0.1)
            gpio.expand_actuator(actuation.actuation_time_to_get_to_angle(h_cfg.max_compression_angle) + 1000, True)
            time.sleep(0.1)
    assert True