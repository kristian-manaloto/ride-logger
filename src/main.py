from gpx_utils import *
import pandas as pd
from speed import findSpeed


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

df = findSpeed(df,time_interval=5)

speeds = df['cspeed'].tolist()

print("max speed using guys code is ", max(speeds), "kmph")