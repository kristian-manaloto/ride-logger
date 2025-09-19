import pandas as pd
import math

# https://physics.stackexchange.com/questions/496046/calculate-acceleration-and-lateral-g-force-from-gps-coordinates
# shout out these people

EARTH_RADIUS = 6371000  # meters
G = 9.81  # gravity in m/s²

def gps_to_xy(lat, lon, lat_ref, lon_ref):
    """Convert lat/lon to local x (east), y (north) in meters"""
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    lat_ref_rad = math.radians(lat_ref)
    lon_ref_rad = math.radians(lon_ref)

    x = (lon_rad - lon_ref_rad) * math.cos(lat_ref_rad) * EARTH_RADIUS
    y = (lat_rad - lat_ref_rad) * EARTH_RADIUS
    return x, y

def compute_velocity(df):
    """
        Compute velocity components and speed from GPS data
        important new column ['velocity'] calculated in meters per second

        args:
            df: dataframe with gpx data

        returns:
            df: copy of dataframe with added x,y,vx,vy, and velocity column     
    """
    df = df.copy()
    lat_ref, lon_ref = df["latitude"].iloc[0], df["longitude"].iloc[0]
    coords = [gps_to_xy(lat, lon, lat_ref, lon_ref) for lat, lon in zip(df["latitude"], df["longitude"])]
    df["x"], df["y"] = zip(*coords)

    dt = df["timestamp"].diff().dt.total_seconds().fillna(1.0)

    df["vx"] = df["x"].diff() / dt
    df["vy"] = df["y"].diff() / dt
    df["velocity"] = (df["vx"]**2 + df["vy"]**2).pow(0.5)
    return df


def extract_fast_accelerations(df, g_threshold=0.5, min_speed_increase=25.0):
    """
    Extract rapid acceleration from the dataframe using the velocity column

    calculates only longitudinal g forces from initial velocity, end velocity and duration

    args:
        df: containing GPX data
        g_threshold: minimum longitudinal G force to consider as fact acceleration
                     default is 0.5 G
        min_speed_increase: minumum speed difference (km/h) in an acceleration to be 
                     included in the returned list

    returns: 
        accelerations: list of dictionaries, each dictionary contains a acceleration segment
    """
    accelerations = []
    in_accel = False
    start_idx = None

    for i in range(1, len(df)):

        start_speed_m_s = df["velocity"].iloc[i-1]
        end_speed_m_s = df["velocity"].iloc[i]
        duration = (df["timestamp"].iloc[i] - df["timestamp"].iloc[i-1]).total_seconds()
        long_g = (end_speed_m_s - start_speed_m_s) / duration / G if duration > 0 else 0

        if long_g >= g_threshold and not in_accel:
            in_accel = True
            start_idx = i - 1
        elif in_accel and (long_g < g_threshold or i == len(df)-1):
            end_idx = i
            in_accel = False

            start_speed = df["velocity"].iloc[start_idx] * 3.6  # m/s → km/h
            end_speed = df["velocity"].iloc[end_idx] * 3.6
            delta_speed = end_speed - start_speed
            duration_total = (df["timestamp"].iloc[end_idx] - df["timestamp"].iloc[start_idx]).total_seconds()

            avg_long_g = (df["velocity"].iloc[end_idx] - df["velocity"].iloc[start_idx]) / duration_total / G if duration_total > 0 else 0

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
                    "duration": duration_total,
                    "longitudinal_g": avg_long_g
                })

    return accelerations