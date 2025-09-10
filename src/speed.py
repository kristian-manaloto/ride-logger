from math import *
import pandas as pd

def lat_long_dist(lat1,lon1,lat2,lon2):
    # function for calculating ground distance between two lat-long locations
    R = 6373.0 # approximate radius of earth in km. 
    lat1 = radians( float(lat1) )
    lon1 = radians( float(lon1) )
    lat2 = radians( float(lat2) )
    lon2 = radians( float(lon2) )
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = round(R * c, 6)
    return distance

def computeDistance(sequencedf):
    prevLat = prevLon = 0 # dummy initiation
    total_dist = 0
    for N in range(len(sequencedf)):
        lat = float(sequencedf.at[N,'latitude'])
        lon = float(sequencedf.at[N,'longitude'])
        if N == 0:
            sequencedf.at[N,'ll_dist'] = 0
        else:
            sequencedf.at[N,'ll_dist'] = lat_long_dist(lat,lon, prevLat,prevLon)
        total_dist += sequencedf.at[N,'ll_dist']
        sequencedf.at[N,'ll_dist_traveled'] = round(total_dist,6)
        prevLat = lat
        prevLon = lon
    return round(total_dist,6)
    # also the original df gets ll_dist and ll_dist_traveled columns added to it

def getTimeOffsets(df, timestamp_col='timestamp'):
    timeOffsets = (df[timestamp_col] - df[timestamp_col].shift()).fillna(pd.Timedelta(seconds=0))
    return timeOffsets.dt.total_seconds().astype(int)

def findSpeed(df, time_interval = 5):    
    computeDistance(df)
    df['offset'] = getTimeOffsets(df)
    df['dspan'] = df['tspan'] = df['cspeed'] = df['diff'] = None
    
    for N in range(len(df)):
        if N == 0: continue
        backi = N
        totOffset = df.at[N,'offset']
        while totOffset <= time_interval*60 :
            backi -= 1
            totOffset += df.at[backi,'offset']
            if backi == 0: break

        tspan = df.at[N,'timestamp'] - df.at[backi,'timestamp']
        df.at[N,'tspan'] = tspan.seconds
        distance = df.at[N,'ll_dist_traveled'] - df.at[backi,'ll_dist_traveled']
        df.at[N,'dspan'] = round(distance,3)
        if distance == 0:
            speed = df.at[N, 'cspeed'] = 0
        else:
            speed = round(distance / tspan.seconds * 3600,2)
            df.at[N, 'cspeed'] = speed
        speed_diff = round(df.at[N,'speed'] - speed, 2)
        df.at[N,'diff'] = speed_diff

    return df

