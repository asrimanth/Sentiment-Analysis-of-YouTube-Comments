import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output

import pandas as pd

from app import app

import components
from sentiment_analysis import sent_analyzer

LAYOUT = html.Div([
    html.Div(id='alert_div_2'),
    html.Br(),
    html.Div(id='table_display_div'),
    dbc.Button("Predict the sentiment", id='get_results', color='success',
                n_clicks=0, outline=True, className="mr-1",
                style={'display':'invisible'}),
    html.Div(id='result_bow'),
    html.Div(id='result_tf_idf')
])


@app.callback(
        [Output('table_display_div', 'children'),
         Output('alert_div_2','children')],
         [Input('memory','data')])
def display_raw_data(df_json):
    if(df_json is not None):
        dataframe = pd.DataFrame(df_json)
        return [html.Div(children=[
            html.H2("The raw data:"),
            components.dark_table(dataframe),
        ]),
            components.timed_alert("Loading last youtube url...", "info", 10)]
    else:
        message = "Please enter a URL to get started."
        return [None, components.timed_alert(message, "warning", 10)]

@app.callback(
        Output('result_bow', 'children'),
        [Input('memory','data'),
         Input('get_results','n_clicks')])
def display_bow(df_json, n_clicks):
    if(n_clicks > 0):
        if(df_json is not None):
            dataframe = pd.DataFrame(df_json)
            result_def = sent_analyzer.return_labeled_df(dataframe)
            
            return html.Div(children=[
                html.H2("The classified data:"),
                components.dark_table_result(result_def),
                # components.timed_alert("Loading last youtube url...", "info", 10)
            ])
