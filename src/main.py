from gpx_utils import *
import pandas as pd
from speed import find_c_speed ,get_max_speed
from display import show_fig
from stops import find_stops,cluster_stops
from acceleration import compute_velocity, extract_fast_accelerations

points = parse_file("data/14-09-2025.gpx")

#time related things
start, end = points[0].time, points[-1].time
duration = end - start
display_time(start, end, duration)

#gpx to dataframe
df = points_to_dataframe(points)

# continous speed over a time frame provides most accurate speed estimate
df = find_c_speed(df)

# instant velocity provides best way to find stops and accelerations
df = compute_velocity(df)


accelerations = extract_fast_accelerations(df)
max_speed_info = get_max_speed(df)

raw_stops = find_stops(df)
clean_stops = cluster_stops(raw_stops)


print(len(raw_stops),len(clean_stops))



show_fig(df,clean_stops,max_speed_info,accelerations)
