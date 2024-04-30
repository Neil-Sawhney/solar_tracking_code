import src.modules.actuation as actuation


def test_get_time_from_test_data():
    angle = -50
    is_expanding = True
    assert actuation._get_time_from_test_data(angle, is_expanding) == 9000

    angle = -32
    assert actuation._get_time_from_test_data(angle, is_expanding) == 8000

    angle = -25
    assert actuation._get_time_from_test_data(angle, is_expanding) == 6500

    angle = -20
    assert actuation._get_time_from_test_data(angle, is_expanding) == 6000

    is_expanding = False
    assert actuation._get_time_from_test_data(angle, is_expanding) == 2975

    angle = -25
    assert actuation._get_time_from_test_data(angle, is_expanding) == 2125

    angle = -32
    assert actuation._get_time_from_test_data(angle, is_expanding) == 425

    angle = 0
    assert actuation._get_time_from_test_data(angle, is_expanding) == 
