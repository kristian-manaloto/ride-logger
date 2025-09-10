from gpx_utils import parse_file, display_time

points = parse_file("data/08-09-2025.gpx")

start, end = points[0].time, points[-1].time
duration = end - start
display_time(start, end, duration)
