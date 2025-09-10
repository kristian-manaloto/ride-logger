from datetime import timedelta
from tzlocal import get_localzone
import gpxpy




def parse_file(path: str):
    """
    Parse a gpx file and return an array of points
    """
    with open(path, 'r', encoding='utf-8') as f:
        gpx = gpxpy.parse(f)


    #data in track
    #track -> segment -> points -> (lat, long, ele, time)

    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            points.extend(segment.points)
     
    return points

def points_to_dataframe(points):
    df = pd.DataFrame({
    'timestamp': [p.time for p in points],
    'latitude': [p.latitude for p in points],
    'longitude': [p.longitude for p in points]
    })

    df = df.sort_values('timestamp').reset_index(drop=True)



def get_ride_times(points):
    """
    Input a list of gpx points
    Return ride start, end, and duration
    """

    if not points:
        return None,None,None
    
    start = points[0].time
    end = points[-1].time
    duration = end - start

    return start, end, duration

def display_time(start,end,duration):
    """
    Display the ride start time, end time, and duration,
    automatically converted to the user's local timezone.
    """
    if not start or not end or not duration:
        print("No time data available.")
        return

    local_tz = get_localzone()

    start_local = start.astimezone(local_tz)
    end_local = end.astimezone(local_tz)

    start_str = start_local.strftime("%Y-%m-%d %H:%M:%S %Z")
    end_str = end_local.strftime("%Y-%m-%d %H:%M:%S %Z")

    # duration as H:M:S
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    print(f"Ride started at : {start_str}")
    print(f"Ride ended at   : {end_str}")
    print(f"Total duration  : {duration_str}")


