import plotly.express as px
import pandas as pd


def show_fig(df: pd.DataFrame):
    fig_1 = px.scatter(df, x='longitude',y='latitude', template='plotly_dark')

    fig_1.show()