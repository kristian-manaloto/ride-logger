import pandas as pd
import numpy as np

def find_fast_accelerations(df, window_sec=5, min_speed_increase=30.0):
    """
    Detect accelerations by checking speed difference over a time window.
    and a minimum speed increase
    """
    df = df.copy()

    # Drop rows with missing required values
    df = df.dropna(subset=['timestamp', 'cspeed', 'latitude', 'longitude']).reset_index(drop=True)

    accelerations = []

    for i in range(len(df)):
        t_start = df['timestamp'].iloc[i]
        start_speed = df['cspeed'].iloc[i]

        # skip invalid start speeds
        if pd.isna(start_speed):
            continue  


        future_points = df[df['timestamp'] >= t_start + pd.Timedelta(seconds=window_sec)]
        if future_points.empty:
            continue
        
        j = future_points.index[0]
        end_speed = df['cspeed'].iloc[j]

        if pd.isna(end_speed):
            continue  

        delta_speed = end_speed - start_speed

        if delta_speed >= min_speed_increase:
            accelerations.append({
                "start_time": t_start,
                "end_time": df['timestamp'].iloc[j],
                "start_lat": df['latitude'].iloc[i],
                "start_lon": df['longitude'].iloc[i],
                "end_lat": df['latitude'].iloc[j],
                "end_lon": df['longitude'].iloc[j],
                "start_speed": start_speed,
                "end_speed": end_speed,
                "duration": (df['timestamp'].iloc[j] - t_start).total_seconds(),
                "delta_speed": delta_speed
            })
    
    return accelerations