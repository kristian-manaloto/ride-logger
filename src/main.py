from gpx_utils import *
import pandas as pd
from speed import find_c_speed,find_instant_speed,get_max_speed
from display import show_fig
from stops import find_stops,cluster_stops
from acceleration import find_fast_accelerations

points = parse_file("data/14-09-2025.gpx")

#time related things
start, end = points[0].time, points[-1].time
duration = end - start
display_time(start, end, duration)

#gpx to dataframe
df = points_to_dataframe(points)
df = find_instant_speed(df)
df = find_c_speed(df,time_interval_sec=30)


raw_stops = find_stops(df)
clean_stops = cluster_stops(raw_stops)


print(len(raw_stops),len(clean_stops))


max_speed_info = get_max_speed(df)


accelerations = find_fast_accelerations(df)

show_fig(df,clean_stops,max_speed_info,accelerations)
