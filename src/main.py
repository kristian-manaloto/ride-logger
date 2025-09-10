from gpx_utils import *

points = parse_file("data/08-09-2025.gpx")

start, end = points[0].time, points[-1].time
duration = end - start
display_time(start, end, duration)

speed_points = get_speed(points)

max_speed = get_max_speed(speed_points)

print("Max speed was: ", max_speed , " kmh")