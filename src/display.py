import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def interpolate_route(df, n_points=500):
    """
        interpolate GPS route data to create less points to scrub through

        args:
            df: with GPX data, lat, long, cspeed
            n_points: number of evenly spaced points to interpolate along the route

        returns:
            df_interp: dataframe with interpolated values
    """
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


def show_fig(df, stops, max_speed_info, accelerations):
    df_interp = interpolate_route(df)

    lats = df_interp['latitude'].tolist()
    lons = df_interp['longitude'].tolist()
    speeds = df_interp['cspeed'].fillna(0.0).tolist()

    # route
    route_trace = go.Scattermapbox(
        lat=df['latitude'], lon=df['longitude'],
        mode='lines', line=dict(width=3, color='red'), name='Route'
    )

    # stops
    stop_lats = [s[1] for s in stops]
    stop_lons = [s[2] for s in stops]
    stop_marker = go.Scattermapbox(
        lat=stop_lats, lon=stop_lons,
        mode='markers+text', marker=dict(size=10, color='blue'),
        textposition='top center', name='Stops'
    )

    # rider
    rider_marker = go.Scattermapbox(
        lat=[lats[0]], lon=[lons[0]],
        mode='markers', marker=dict(size=10, color='green'), name='Rider'
    )

    # max speed
    max_speed = max_speed_info[0]
    max_speed_lat = max_speed_info[1]
    max_speed_lon = max_speed_info[2]
    max_speed_marker = go.Scattermapbox(
        lat=[max_speed_lat], lon=[max_speed_lon],
        mode='markers', hovertext=f"{max_speed:.1f} km/h",
        marker=dict(size=14, color='lime'), name='Max Speed'
    )

    # accelerations
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
                f"Start speed: {accel['start_speed']:.1f} km/h<br>"
                f"End speed: {accel['end_speed']:.1f} km/h<br>"
                f"Duration: {accel['duration']:.1f}s<br>"
                f"Longitudinal G: {accel['longitudinal_g']:.2f}<br>"
            )
        )
        accel_traces.append(trace)

    # speed display
    speed_annotation = dict(
        text=f"Speed: {speeds[0]:.1f} km/h",
        x=0, y=1, xref='paper', yref='paper',
        xanchor='left', yanchor='top',
        showarrow=False, font=dict(size=16, color='black')
    )

    # slider to update the rider and speed

    data =[route_trace, stop_marker, rider_marker, max_speed_marker] + accel_traces

    rider_index = 2  # index of rider trace in data list above
    steps = []
    for i in range(len(df_interp)):
        # update rider marker only
        step_rider = dict(
            method="restyle",
            args=[{"lat": [[lats[i]]], "lon": [[lons[i]]]}, [rider_index]],
            label=str(i)
        )
        steps.append(step_rider)

        # update annotation only
        step_annotation = dict(
            method="relayout",
            args=[{"annotations[0].text": f"Speed: {speeds[i]:.1f} km/h"}],
            label=str(i)
        )
        steps.append(step_annotation)

    sliders = [dict(active=0, currentvalue={"prefix": "Point: "}, pad={"t": 50}, steps=steps)]

    # figure
    fig = go.Figure(
        data=data,
        layout=go.Layout(
            mapbox=dict(
                style='open-street-map',
                center=dict(lat=df['latitude'].mean(), lon=df['longitude'].mean()),
                zoom=13
            ),
            annotations=[speed_annotation],
            sliders=sliders,
            margin=dict(l=0, r=0, t=0, b=0)
        )
    )

    fig.show()