import pandas as pd
import numpy as np
import math

# https://physics.stackexchange.com/questions/496046/calculate-acceleration-and-lateral-g-force-from-gps-coordinates
# shout out these people

EARTH_RADIUS = 6371000  # meters
G = 9.81  # gravity in m/s²


def gps_to_xy(lat, lon, lat_ref, lon_ref):
    """
    Convert lat/lon to local x (east), y (north) coordinates in meters
    using equirectangular approximation.
    """
    lat = math.radians(lat)
    lon = math.radians(lon)
    lat_ref = math.radians(lat_ref)
    lon_ref = math.radians(lon_ref)

    x = (lon - lon_ref) * math.cos(lat_ref) * EARTH_RADIUS
    y = (lat - lat_ref) * EARTH_RADIUS
    return x, y

def compute_velocity_and_g(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute velocity, speed, acceleration, and G-forces from a DataFrame
    with 'timestamp', 'latitude', 'longitude'.
    
    Returns a modified DataFrame with extra columns: vx, vy, speed, ax, ay, 
    longitudinal_accel, lateral_accel, longitudinal_g, lateral_g.
    """
    df = df.copy()
    lat_ref, lon_ref = df["latitude"].iloc[0], df["longitude"].iloc[0]


    coords = [gps_to_xy(lat, lon, lat_ref, lon_ref) for lat, lon in zip(df["latitude"], df["longitude"])]
    df["x"], df["y"] = zip(*coords)

    dt = df["timestamp"].diff().dt.total_seconds().fillna(1.0)

    # velocity (m/s)
    df["vx"] = df["x"].diff() / dt
    df["vy"] = df["y"].diff() / dt

    # speed but in m/s
    df["speed"] = (df["vx"]**2 + df["vy"]**2).pow(0.5)

    # acceleration in m/s^2
    df["ax"] = df["vx"].diff() / dt
    df["ay"] = df["vy"].diff() / dt

    # longitudinal & lateral accelerations
    df["longitudinal_accel"] = (df["ax"] * df["vx"] + df["ay"] * df["vy"]) / df["speed"].replace(0, 1)
    df["lateral_accel"] = (df["ax"] * df["vy"] - df["ay"] * df["vx"]) / df["speed"].replace(0, 1)

    # convert to G-forces
    df["longitudinal_g"] = df["longitudinal_accel"] / G
    df["lateral_g"] = df["lateral_accel"] / G

    # replace NaN / inf with 0
    df = df.fillna(0)
    df = df.replace([math.inf, -math.inf], 0)
    df = df.infer_objects()

    return df

def extract_fast_accelerations(df: pd.DataFrame, g_threshold=0.5, min_speed_increase=20.0):
    """
    Extract rapid acceleration segments from a DataFrame computed by
    compute_velocity_and_g().
    
    Returns a list of dicts with:
        start_lat, start_lon, end_lat, end_lon,
        start_speed, end_speed, delta_speed,
        start_time, end_time, duration,
        longitudinal_g, lateral_g
    """
    accelerations = []
    in_accel = False
    start_idx = None

    for i in range(1, len(df)):
        g = df["longitudinal_g"].iloc[i]

        if g >= g_threshold and not in_accel:
            in_accel = True
            start_idx = i - 1
        elif in_accel and (g < g_threshold or i == len(df) - 1):
            end_idx = i
            in_accel = False

            start_speed = df["speed"].iloc[start_idx] * 3.6  # m/s → km/h
            end_speed = df["speed"].iloc[end_idx] * 3.6
            delta_speed = end_speed - start_speed
            duration = (df["timestamp"].iloc[end_idx] - df["timestamp"].iloc[start_idx]).total_seconds()

            if delta_speed >= min_speed_increase:
                accelerations.append({
                    "start_lat": df["latitude"].iloc[start_idx],
                    "start_lon": df["longitude"].iloc[start_idx],
                    "end_lat": df["latitude"].iloc[end_idx],
                    "end_lon": df["longitude"].iloc[end_idx],
                    "start_speed": start_speed,
                    "end_speed": end_speed,
                    "delta_speed": delta_speed,
                    "start_time": df["timestamp"].iloc[start_idx],
                    "end_time": df["timestamp"].iloc[end_idx],
                    "duration": duration,
                    "longitudinal_g": df["longitudinal_g"].iloc[start_idx],
                    "lateral_g": df["lateral_g"].iloc[start_idx]
                })

    return accelerations