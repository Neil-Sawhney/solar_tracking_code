import time

import src.helpers.gpio as gpio
import src.helpers.hardware_config as h_cfg
import src.modules.actuation as actuation


def test_home_actuator():
    gpio.home_actuator()
    assert True


def test_contraction_consistency():
    # Test the consistency of the desired angle by going repeatedly from max_expansion_angle to every angle in between to max_compression_angle in 1 degree increments
    num_of_tests = 10
    angle_list = [
        (425, -32.6),
        (850, -30.7),
        (1275, -28.7),
        (1700, -26.3),
        (2125, -23.9),
        (2550, -21.4),
        (2975, -18.8),
        (3400, -15.7),
        (3825, -12.4),
        (4250, -8.9),
        (4675, -5.0),
        (5100, -1.1),
        (5525, 3.7),
        (5950, 8.2),
        (6375, 12.7),
        (6800, 17.3),
        (7225, 21.4),
        (7650, 25.9),
        (8075, 29.4),
        (8500, 30.4),
    ]
    for _ in range(num_of_tests):
        for actuation_time, angle in angle_list:
            # contract the actuator to the desired angle
            gpio.contract_actuator(actuation_time)
            print("Contracting actuator to", angle)

            # home the actuator
            time.sleep(0.1)
            gpio.home_actuator()
            time.sleep(0.1)
    assert True


def test_expansion_consistency():
    # Test the consistency of the desired angle by going repeatedly from max_compression_angle to every angle in between to max_expansion_angle in 1 degree increments
    num_of_tests = 10
    angle_list = [
        (0, -35.3),
        (425, -32.6),
        (850, -30.7),
        (1275, -28.7),
        (1700, -26.3),
        (2125, -23.9),
        (2550, -21.4),
        (2975, -18.8),
        (3400, -15.7),
        (3825, -12.4),
        (4250, -8.9),
        (4675, -5.0),
        (5100, -1.1),
        (5525, 3.7),
        (5950, 8.2),
        (6375, 12.7),
        (6800, 17.3),
        (7225, 21.4),
        (7650, 25.9),
        (8075, 29.4),
        (8500, 30.4),
    ]

    for _ in range(num_of_tests):
        for actuation_time, angle in angle_list:
            # expand the actuator to the desired angle
            gpio.expand_actuator(actuation_time)
            print("Expanding actuator to", angle)

            # home the actuator
            time.sleep(0.1)
            gpio.home_actuator()
            time.sleep(0.1)
    assert True
