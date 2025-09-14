import plotly.graph_objects as go


def show_fig(df,stops):

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

    rider_marker = go.Scattermapbox(
        lat=[df['latitude'].iloc[0]],
        lon=[df['longitude'].iloc[0]],
        mode="markers",
        marker=dict(size=14, color='green'),
        name="Rider"
    )


    fig = go.Figure(data=[route_trace, stop_marker ,rider_marker])

    steps = []

    for i in range(len(df)):
        step = dict(
            method="restyle",  
            args=[{"lat": [[df['latitude'].iloc[i]]], 
                "lon": [[df['longitude'].iloc[i]]]}, 
                [2]], 
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