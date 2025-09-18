import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def interpolate_route(df, n_points=500):
    df = df.copy()
    distances = np.zeros(len(df))
    for i in range(1, len(df)):
        distances[i] = distances[i-1] + np.sqrt(
            (df['latitude'].iloc[i] - df['latitude'].iloc[i-1])**2 +
            (df['longitude'].iloc[i] - df['longitude'].iloc[i-1])**2
        )

    lat_interp_func = interp1d(distances, df['latitude'], kind='linear')
    lon_interp_func = interp1d(distances, df['longitude'], kind='linear')
    speed_interp_func = interp1d(distances, df['cspeed'], kind='linear')

    dist_new = np.linspace(0, distances[-1], n_points)
    df_interp = pd.DataFrame({
        'latitude': lat_interp_func(dist_new),
        'longitude': lon_interp_func(dist_new),
        'cspeed': speed_interp_func(dist_new)
    })
    return df_interp


def show_fig(df,stops,max_speed_info,accelerations):
    df_interp = interpolate_route(df,500)

    #draw the route
    route_trace = go.Scattermapbox(lat=df['latitude'],lon=df['longitude'],
        mode='lines',line=dict(width=3, color='red'),name="Route"
    )

    #mark the stops
    lats = [s[1] for s in stops]
    lons = [s[2] for s in stops]

    stop_marker = go.Scattermapbox(
        mode="markers+text",
        lat = lats,
        lon = lons,
        marker=dict(size=10, color='blue'),
        textposition="top center",
        name="Stops"
    )

    #rider
    rider_marker = go.Scattermapbox(
        lat=[df['latitude'].iloc[0]],
        lon=[df['longitude'].iloc[0]],
        mode="markers",
        marker=dict(size=10, color='green'),
        name="Rider"
    )

    #max speed
    max_speed = max_speed_info[0]
    max_speed_lat = max_speed_info[1]
    max_speed_long = max_speed_info[2]

    max_speed_marker = go.Scattermapbox(
        lat=[max_speed_lat],
        lon=[max_speed_long],
        mode="markers",
        hovertext=max_speed,
        marker=dict(size=14, color='lime'),
        name="Max Speed"
    )

    accel_traces = []
    for accel in accelerations:
        trace = go.Scattermapbox(
            lat=[accel['start_lat'], accel['end_lat']],
            lon=[accel['start_lon'], accel['end_lon']],
            mode='lines+markers',
            line=dict(width=4, color='purple'),
            marker=dict(size=8, color='purple'),
            name=f"{accel['delta_speed']:.1f} km/h",
            hovertemplate=(
                f"Start: {accel['start_speed']:.1f} km/h<br>"
                f"End: {accel['end_speed']:.1f} km/h<br>"
                f"Duration: {accel['duration']:.1f}s"
            )
        )
        accel_traces.append(trace)


    fig = go.Figure(data=[route_trace, stop_marker ,rider_marker,max_speed_marker] + accel_traces)

    steps = []
    for i in range(len(df_interp)):
        step = dict(
            method="restyle",
            args=[{
                "lat": [[df_interp['latitude'].iloc[i]]],
                "lon": [[df_interp['longitude'].iloc[i]]]
            }, [2]],
            label=str(i)
        )
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 50}, steps=steps)]

    fig.update_layout(
        sliders=sliders,
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=df['latitude'].mean(), lon=df['longitude'].mean()),
            zoom=13
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    fig.show()