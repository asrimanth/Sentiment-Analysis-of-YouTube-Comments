import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output

import plotly.express as px

import pandas as pd

from app import app

import components
from location import loc_utils

LAYOUT = html.Div([
    html.Div(id='alert_div_3'),
    html.H2("Location-based sentiment metric in the US"),
    html.Br(),
    dcc.Graph(id="location_display_graph"),
    # html.Div(id='Location_display_div'),
])


@app.callback(
        [Output('location_display_graph', 'figure'),
         Output('alert_div_3','children')],
         [Input('memory','data')])
def display_location_data(df_json):
    if(df_json is not None):
        dataframe = pd.DataFrame(df_json)
        loc_series = loc_utils.return_locations(dataframe)
        fig = px.choropleth(locations=loc_series.index, locationmode="USA-states", color=list(range(0,51)), 
        scope="usa", color_continuous_scale="Viridis")
        return [fig, 
            components.timed_alert("Loading last youtube url...", "info", 10)]
    else:
        message = "Please enter a URL to get started."
        return [None, components.timed_alert(message, "warning", 10)]
