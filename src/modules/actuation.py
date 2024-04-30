import numpy as np
import pandas as pd

import helpers.hardware_config as h_cfg


def follow_plan(plan):
    """moves the actuator according to the plan, which is a pandas.Series of actuation times milliseconds for each time. The actuator will move at a constant speed to the next position according to update_interval defined in user_config. Blocks until the end of the plan.

    Args:
        plan (pandas.Series): The actuation times of the actuator in milliseconds for each time.

    """
    # TODO: Implement this function
    # if the time
    pass


def actuation_time_to_get_to_angle(angles):
    """Converts the desired rotation angle of the tracker to the required time to keep the actuator on to get from each angle to the next.

    Args:
        angles (pandas.Series): dict or DataFrame with the following columns:
            * `tracker_theta`: The rotation angle of the tracker is a right-handed
            rotation defined by `roof_heading`.
            tracker_theta = 0 is horizontal. [degrees]
            * `aoi`: The angle-of-incidence of direct irradiance onto the
            rotated panel surface. [degrees]
            * `surface_tilt`: The angle between the panel surface and the earth
            surface, accounting for panel rotation. [degrees]
            * `surface_azimuth`: The azimuth of the rotated panel, determined by
            projecting the vector normal to the panel's surface to the earth's
            surface. [degrees]

    Returns:
        pandas.Series: The time to keep the actuator on to get to the next angle in the plan.


    """

    # FIXME: edge cases
    # FIXME: add a column for expanding or contracting
    # make a column for actuation time
    angles["actuation_time"] = 0
    actuation_time_index = angles.columns.get_loc("actuation_time")

    if not np.isnan(angles.iloc[0]["tracker_theta"]):
        is_contracting = (
            True if angles.iloc[0]["tracker_theta"] > -h_cfg.max_angle else False
        )
        is_expanding = not is_contracting

        angles.iat[0, actuation_time_index] = _get_time_from_test_data(
            angles.iloc[0]["tracker_theta"], is_expanding
        )

    for i in range(1, len(angles)):
        # get the angle
        angle = angles.iloc[i]["tracker_theta"]

        # get the previous angle
        prev_angle = angles.iloc[i - 1]["tracker_theta"]

        if np.isnan(angle) or np.isnan(prev_angle):
            continue

        is_expanding = True if angle < prev_angle else False

        # get the time it takes to get to the angle
        actuation_time = _get_time_from_test_data(
            angle, is_expanding
        ) - _get_time_from_test_data(prev_angle, is_expanding)

        # add the time to the series
        angles.iat[i, actuation_time_index] = actuation_time

    return angles


def _get_time_from_test_data(angle, is_expanding):
    """Pull from test data to get the time it takes to get the actuator to a certain angle.

    Args:
        angle (int): angle in degrees
        is_expanding (bool): True if the actuator is expanding, False if contracting

    Returns:
        float: time in milliseconds
    """
    if is_expanding:
        df = pd.read_csv("src/helpers/expansion.csv", header=0)
    else:
        df = pd.read_csv("src/helpers/contraction.csv", header=0)

    angle_list = df["theta"].values

    # Find the closest angle in the data
    angle_small = min(angle_list, key=lambda x: abs(x - angle))
    angle_big = max(angle_list, key=lambda x: abs(x - angle))

    time_small = df["t"].loc[df["theta"] == angle_small].values[0]
    time_big = df["t"].loc[df["theta"] == angle_big].values[0]

    time = np.interp(angle, [angle_small, angle_big], [time_small, time_big])

    return time
