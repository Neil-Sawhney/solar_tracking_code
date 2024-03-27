import actuation
import matplotlib.pyplot as plt
import pandas as pd
from pvlib import solarposition, tracking

import helpers.efficiency as efficiency
import helpers.hardware_config as hardware_config
import user_config


def get_daily_plan():
    """Determine the displacement of the linear actuator for all times from the current time to midnight.

    Returns:
    pandas.Series: The displacement of the actuator in millimeters for each time.
    """
    today = pd.Timestamp.now(tz=user_config.time_zone)
    times = pd.date_range(
        today, today + pd.Timedelta(days=1), freq="5min", tz=user_config.tz
    )
    angles = get_angles(times)

    tracker_angles = efficiency.optimize_tracker_angles(angles)

    displacements = actuation.angle_to_displacement(tracker_angles)


def get_angles(times):
    """Determine the rotation angle for all times, along with the angle of incidence of the sun on the panel.

    Args:
    times (pandas.DatetimeIndex): Times at which to calculate the angles.

    Returns:
    dict or DataFrame with the following columns:
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
    """
    solpos = solarposition.get_solarposition(times, user_config.lat, user_config.lon)

    truetracking_angles = tracking.singleaxis(
        apparent_zenith=solpos["apparent_zenith"],
        apparent_azimuth=solpos["azimuth"],
        axis_tilt=user_config.roof_angle,
        axis_azimuth=user_config.roof_heading,
        max_angle=hardware_config.max_angle,
        backtrack=False,  # for true-tracking
    )

    return truetracking_angles
