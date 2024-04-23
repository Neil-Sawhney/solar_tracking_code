def follow_plan(plan):
    """moves the actuator according to the plan, which is a pandas.Series of displacements in millimeters for each time. The actuator will move at a constant speed to the next position according to update_interval defined in user_config. Blocks until the end of the plan.

    Args:
        plan (pandas.Series): The displacement of the actuator in millimeters for each time.

    """
    # TODO: Implement this function
    pass


def time_to_get_to_angle(angles):
    """Converts the desired rotation angle of the tracker to the required time to keep the actuator on for to get from each angle to the next.

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
    # TODO: Implement this function
    pass
