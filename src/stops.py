import pandas as pd

def find_stops(df):
    """
    looks at any period where speed was less than 4kmph, and marks it as a stop

    args:
        df: data fram with gpx data
    returns: 
        stops: an array of tuples containing stop information (time, lat, long)
    """

    df = df.copy()
    
    zero_speed_rows = df[df["velocity"] <= 4]

    stops = [(row["timestamp"], row["latitude"], row["longitude"]) 
             for _, row in zero_speed_rows.iterrows()]


    return stops

def cluster_stops(stops, threshold=0.001):
    """
    iterate over each stop and combine
    multiple stop points within a threshold and turns them into a single stop

    args:
        stops: an array of raw stop points
        threshold: long and lat degree to combine points by

    returns:
        clustered: an array of combined stop points
    """

    if not stops:
        return []

    clustered = []
    current_cluster = [stops[0]]

    for stop in stops[1:]:
        _, lat, lon = stop
        _, prev_lat, prev_lon = current_cluster[-1]

        # same cluster if within threshold
        if abs(lat - prev_lat) <= threshold and abs(lon - prev_lon) <= threshold:
            current_cluster.append(stop)

        else:
            # finalize with the *last* stop in the cluster
            clustered.append(current_cluster[-1])
            current_cluster = [stop]

    # finalize last cluster
    clustered.append(current_cluster[-1])

    return clustered
