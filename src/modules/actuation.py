import numpy as np
import pandas as pd

import helpers.gpio as gpio
import helpers.hardware_config as h_cfg


def follow_plan(plan):
    """moves the actuator according to the plan, which is a pandas.Series of actuation times milliseconds for each time. The actuator will move at a constant speed to the next position according to update_interval defined in user_config. Blocks until the end of the plan.

    Args:
        plan (pandas.Series): The actuation times of the actuator in milliseconds for each time.

    """
    current_plan_index = 0
    current_time = pd.Timestamp.now(tz=h_cfg.time_zone)
    next_move_time = plan.index[current_plan_index + 1]

    while current_time < plan.index[-1]:
        current_time = pd.Timestamp.now(tz=h_cfg.time_zone)

        if current_time >= next_move_time:
            current_plan_index += 1
            next_move_time = plan.index[current_plan_index + 1]

            actuation_time = plan.iloc[current_plan_index]
            is_expanding = plan.iloc[current_plan_index]["is_expanding"]

            if is_expanding:
                gpio.expand_actuator(actuation_time)
            else:
                gpio.contract_actuator(actuation_time)


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

    # make a column for actuation time and is_expanding
    angles["actuation_time"] = 0
    angles["is_expanding"] = 0

    if not np.isnan(angles.iloc[0]["tracker_theta"]):

        # if tracker_theta > max_compression_angle set tracker_theta to max_compression_angle
        if angles.iloc[0]["tracker_theta"] > h_cfg.max_compression_angle:
            angles.iat[0, angles.columns.get_loc("tracker_theta")] = (
                h_cfg.max_compression_angle
            )
        # else if tracker_theta < max_expansion_angle set tracker_theta to max_expansion_angle
        elif angles.iloc[0]["tracker_theta"] < h_cfg.max_expansion_angle:
            angles.iat[0, angles.columns.get_loc("tracker_theta")] = (
                h_cfg.max_expansion_angle
            )

        is_contracting = (
            True if angles.iloc[0]["tracker_theta"] >= -h_cfg.max_angle else False
        )
        is_expanding = not is_contracting

        angles.iat[0, angles.columns.get_loc("actuation_time")] = (
            _get_time_from_test_data(angles.iloc[0]["tracker_theta"], is_expanding)
        )
        angles.iat[0, angles.columns.get_loc("is_expanding")] = int(is_expanding)

    for i in range(1, len(angles)):
        # get the angle
        angle = angles.iloc[i]["tracker_theta"]
        prev_angle = angles.iloc[i - 1]["tracker_theta"]

        # if tracker_theta > max_compression_angle set tracker_theta to max_compression_angle
        if angle > h_cfg.max_compression_angle:
            angles.iat[i, angles.columns.get_loc("tracker_theta")] = (
                h_cfg.max_compression_angle
            )
            angle = h_cfg.max_compression_angle
        # else if tracker_theta < max_expansion_angle set tracker_theta to max_expansion_angle
        elif angle < h_cfg.max_expansion_angle:
            angles.iat[i, angles.columns.get_loc("tracker_theta")] = (
                h_cfg.max_expansion_angle
            )
            angle = h_cfg.max_expansion_angle

        if np.isnan(angle) or np.isnan(prev_angle):
            continue

        is_expanding = True if angle < prev_angle else False

        # get the time it takes to get to the angle
        actuation_time = _get_time_from_test_data(
            angle, is_expanding
        ) - _get_time_from_test_data(prev_angle, is_expanding)

        # add the time to the series
        angles.iat[i, angles.columns.get_loc("actuation_time")] = actuation_time
        angles.iat[i, angles.columns.get_loc("is_expanding")] = int(is_expanding)

    return angles


def _get_time_from_test_data(angle, is_expanding):
    """Pull from test data to get the time it takes to get the actuator to a certain angle.

    Args:
        angle (int): angle in degrees
        is_expanding (bool): True if the actuator is expanding, False if contracting

    Returns:
        int: time in milliseconds
    """
    if is_expanding:
        df = pd.read_csv("src/helpers/expansion.csv", header=0)
    else:
        df = pd.read_csv("src/helpers/contraction.csv", header=0)

    angle_list = df["theta"].values

    # Find the closest angle in the data before and after the desired angle
    angle_small = angle_list[angle_list <= angle].max()
    angle_big = angle_list[angle_list >= angle].min()

    time_small = df["t"].loc[df["theta"] == angle_small].values[0]
    time_big = df["t"].loc[df["theta"] == angle_big].values[0]

    time = np.interp(angle, [angle_small, angle_big], [time_small, time_big])

    return int(time)
