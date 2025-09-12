from gpx_utils import *
import pandas as pd
from speed import findSpeed
from display import show_fig
from stops import find_stops

points = parse_file("data/08-09-2025.gpx")

start, end = points[0].time, points[-1].time
duration = end - start
display_time(start, end, duration)

df = pd.DataFrame({
    'timestamp': [p.time for p in points],
    'latitude': [p.latitude for p in points],
    'longitude': [p.longitude for p in points]
})

df = df.sort_values('timestamp').reset_index(drop=True)

speed = findSpeed(df,time_interval_sec=30)

speeds = df['cspeed'].tolist()
valid_speeds = [s for s in speeds if s is not None]  

print("Max speed:", max(valid_speeds), "km/h")

find_stops(df,5,10)

show_fig(df)
