import time

import src.helpers.gpio as gpio
import src.helpers.hardware_config as h_cfg
import src.modules.actuation as actuation


def test_contraction_consistency():
    # Test the consistency of the desired angle by going repeatedly from max_expansion_angle to every angle in between to max_compression_angle in 1 degree increments
    num_of_tests = 10
    for _ in range(num_of_tests):
        angle_list = [
            -35.3,
            -32.6,
            -30.7,
            -28.7,
            -26.3,
            -23.9,
            -21.4,
            -18.8,
            -15.7,
            -12.4,
            -8.9,
            -5.0,
            -1.1,
            3.7,
            8.2,
            12.7,
            17.3,
            21.4,
            25.9,
            29.4,
            30.4,
        ]
        for angle in angle_list:
            # contract the actuator to the desired angle
            gpio.contract_actuator(
                actuation.actuation_time_to_get_to_angle(angle, False)
            )

            # home the actuator
            time.sleep(0.1)
            gpio.contract_actuator(
                actuation.actuation_time_to_get_to_angle(h_cfg.max_expansion_angle)
                + 1000,
                True,
            )
            time.sleep(0.1)
    assert True


def test_expansion_consistency():
    # Test the consistency of the desired angle by going repeatedly from max_compression_angle to every angle in between to max_expansion_angle in 1 degree increments
    num_of_tests = 10
    angle_list = [
        30.4,
        28.5,
        23.5,
        18.5,
        13.5,
        8.5,
        3.4,
        -1.4,
        -6.0,
        -10.2,
        -14.0,
        -17.5,
        -21.2,
        -24.3,
        -27.0,
        -29.4,
        -31.5,
        -33.5,
        -35.3,
    ]
    for _ in range(num_of_tests):
        for angle in angle_list:
            # expand the actuator to the desired angle
            gpio.expand_actuator(actuation.actuation_time_to_get_to_angle(angle, True))

            # home the actuator
            time.sleep(0.1)
            gpio.expand_actuator(
                actuation.actuation_time_to_get_to_angle(h_cfg.max_compression_angle)
                + 1000,
                True,
            )
            time.sleep(0.1)
    assert True
