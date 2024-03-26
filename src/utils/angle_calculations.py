import matplotlib.pyplot as plt
import pandas as pd
from pvlib import solarposition, tracking

tz = "US/Eastern"
lat, lon = 40, -80  # TODO: customize this for your location
# TODO: use irradiance data for today

times = pd.date_range(
    "2019-01-01", "2019-01-02", freq="5min", tz=tz
)  # TODO: every day in the morning compute this for the rest of the day
solpos = solarposition.get_solarposition(times, lat, lon)

truetracking_angles = tracking.singleaxis(
    apparent_zenith=solpos["apparent_zenith"],
    apparent_azimuth=solpos["azimuth"],
    # TODO: these need to be changed for roof position and max angle of our setup, make an object that stores all the UDFs
    axis_tilt=0,
    axis_azimuth=180,
    max_angle=90,
    backtrack=False,  # for true-tracking
    gcr=0.5,  # irrelevant for true-tracking
)

# TODO: incorporate roof angle!
truetracking_position = truetracking_angles["tracker_theta"]
