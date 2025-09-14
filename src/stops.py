import pandas as pd

def find_stops(df):
    """
    Given the dataframe, looks at any period where speed was less than 
    4kmph, and marks it as a stop

    returns an array of tuples containing stop information (time, lat, long)
    """

    df = df.copy()
    
    zero_speed_rows = df[df["inst_speed"] <= 4]

    stops = [(row["timestamp"], row["latitude"], row["longitude"]) 
             for _, row in zero_speed_rows.iterrows()]


    return stops

def cluster_stops(stops, threshold=0.0002):
    if not stops:
        return []

    clustered = []
    current_cluster = [stops[0]]

    for stop in stops[1:]:
        _, lat, lon = stop
        _, prev_lat, prev_lon = current_cluster[-1]

        # If close to previous point, add to current cluster
        if abs(lat - prev_lat) <= threshold and abs(lon - prev_lon) <= threshold:
            current_cluster.append(stop)
        else:

            lats = [s[1] for s in current_cluster]
            lons = [s[2] for s in current_cluster]
            start_time = current_cluster[0][0]
            end_time   = current_cluster[-1][0]
            mean_lat = sum(lats) / len(lats)
            mean_lon = sum(lons) / len(lons)
            clustered.append((start_time, end_time, mean_lat, mean_lon))

            current_cluster = [stop]

    lats = [s[1] for s in current_cluster]
    lons = [s[2] for s in current_cluster]
    start_time = current_cluster[0][0]
    end_time   = current_cluster[-1][0]
    mean_lat = sum(lats) / len(lats)
    mean_lon = sum(lons) / len(lons)
    clustered.append((start_time, end_time, mean_lat, mean_lon))

    return clustered
