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


LAYOUT = html.Div([
    html.Div(id='alert_div_4'),
    html.H2("Bag of Words"),
    html.Br(),
    html.Div(id='bow_metric'),
    html.Br(),
    html.H2("TF-IDF"),
    html.Br(),
    html.Div(id='tf_idf_metric'),
    html.Br(),
    html.H2("Performance Comparision charts"),
    html.Br(),
    html.Div(id='model_comp_div'),
])

@app.callback(
        [Output('bow_metric', 'children'),
         Output('tf_idf_metric', 'children'),
         Output('model_comp_div','children')],
         [Input('memory','data')])
def  display_results(data):
    df1 = pd.read_excel('bow.xlsx')
    df2 = pd.read_excel('tf-idf.xlsx')
    df3 = pd.read_excel('model_comparision.xlsx')
    return (components.dark_table(df1,width='1000px'),
            components.dark_table(df2,width='1000px'),
            components.dark_table(df3,width='1000px'))

