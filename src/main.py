from gpx_utils import *
import pandas as pd
from speed import findSpeed,find_instant_speed
from display import show_fig
from stops import find_stops

points = parse_file("data/08-09-2025.gpx")

start, end = points[0].time, points[-1].time
duration = end - start
display_time(start, end, duration)

df = points_to_dataframe(points)
df = find_instant_speed(df)

speed = findSpeed(df,time_interval_sec=30)

speeds = df['cspeed'].tolist()

rawspeed = df['inst_speed'].tolist()

valid_speeds = [s for s in speeds if s is not None]  

print("Max speed:", max(valid_speeds), "km/h")

stops = find_stops(df,4,5)

show_fig(df,stops)
