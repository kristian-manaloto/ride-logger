import pandas as pd

def find_stops(df, threshold, min_duration):
    df = df.copy()
    speed_col = "cspeed"

    df["stopped"] = df[speed_col] < threshold

    stops = []
    in_stop = False
    start_time = None

    for t, row in df.iterrows():
        if row["stopped"] and not in_stop:
            in_stop = True
            start_time = row["timestamp"]
        elif not row["stopped"] and in_stop:
            stop_duration = (row["timestamp"] - start_time).total_seconds()
            if stop_duration >= min_duration:
                stops.append((row['timestamp'],row['latitude'],row['longitude']))

            in_stop = False 
    

    for frame in stops:
       print(frame)

    return stops