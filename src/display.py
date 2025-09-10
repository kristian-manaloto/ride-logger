import plotly.graph_objects as go

def show_fig(df):

    route_trace = go.Scattermapbox(lat=df['latitude'],lon=df['longitude'],
        mode='lines',line=dict(width=3, color='red'),name="Route"
    )

    fig = go.Figure(route_trace)

    fig.update_layout(
        mapbox=dict(style="open-street-map",
            center=dict(lat=df['latitude'].mean(), lon=df['longitude'].mean()),
            zoom=12
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    fig.show()