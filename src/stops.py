import pandas as pd

def find_stops(df):

    df = df.copy()
    
    zero_speed_rows = df[df["inst_speed"] <= 4]

    stops = [(row["timestamp"], row["latitude"], row["longitude"]) 
             for _, row in zero_speed_rows.iterrows()]


    for stop in stops:
       print(stop)

    return stops