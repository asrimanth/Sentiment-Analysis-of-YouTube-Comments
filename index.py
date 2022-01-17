import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from data_extraction import ytube_url_ui as yui
from sentiment_analysis import sentiment_ui as sui
from location import loc_disp as lui
from metrics import met_disp as mui
import pandas as pd
import plotly.express as px

from app import app

tab_selected_style = {
    'backgroundColor': '#4FC3F7',
    'border': '#4FC3F7'
}

'''
The overall layout of the app.
'''
app.layout = html.Div([
    dcc.Tabs(id='tab-group', value='tab-0', children=[
        dcc.Tab(label='Youtube data', value='tab-0',selected_style = tab_selected_style),
        dcc.Tab(label='Sentiment', value='tab-1',selected_style = tab_selected_style),
        dcc.Tab(label='Location', value='tab-2',selected_style = tab_selected_style),
        dcc.Tab(label='Metrics', value='tab-3',selected_style = tab_selected_style),
    ], colors={
        "border": "#4FC3F7"
    }),
    dcc.Store(id='memory'),
    dcc.Store(id='sent_analyzed_df'),
    html.Div(id='tab_content',children=[
        html.H3("Hello world")
    ])
])

@app.callback(Output('tab_content', 'children'),
              [Input('tab-group', 'value')])
def render_content(tab_id):
    """Method which renders the content by returning contents of different layouts.

    Arguments:
        tab_id {str} -- The id of the tab which is currently selected.

    Returns:
        list -- A list of components as defined in each layout file.
    """
    if tab_id == 'tab-0':
        return yui.LAYOUT
    elif tab_id == 'tab-1':
        return sui.LAYOUT
    elif tab_id == 'tab-2':
        return lui.LAYOUT
    elif tab_id == 'tab-3':
        return mui.LAYOUT

if(__name__ == '__main__'):
    app.run_server(debug=True)
