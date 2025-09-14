import plotly.graph_objects as go

def show_fig(df,stops):

    #draw the route
    route_trace = go.Scattermapbox(lat=df['latitude'],lon=df['longitude'],
        mode='lines',line=dict(width=3, color='red'),name="Route"
    )

    #mark the stops
    lats = [s[1] for s in stops]
    lons = [s[2] for s in stops]

    mark_stops = go.Scattermapbox(
        mode="markers+text",
        lat = lats,
        lon = lons,
        marker=dict(size=10, color='blue'),
        textposition="top center",
        name="Stops"
    )

    fig = go.Figure(data=(route_trace,mark_stops))

    fig.update_layout(
        mapbox=dict(style="open-street-map",
            center=dict(lat=df['latitude'].mean(), lon=df['longitude'].mean()),
            zoom=12
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    fig.show()