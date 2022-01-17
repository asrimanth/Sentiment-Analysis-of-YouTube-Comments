"""A module which is used as a tab in the dash app.
    It displays the dataframe of comments from the input youtube url.

Returns:
    None -- Does not return anything.
    However, the variable 'LAYOUT' can be imported into any dash app.
"""

import sys
import dash_bootstrap_components as dbc
import dash_html_components as html
import googleapiclient.errors as api_err
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import components
import error_utils

from data_extraction import url_data_extract as backend
from app import app


sys.path.append('..')


LAYOUT = html.Div([
    html.H3("Welcome!", style={'textAlign': 'center'}),
    html.Div(id='alert_div',style={'margin': '20px'}),
    dbc.Input(
        id='url_textarea',
        placeholder="Enter a valid youtube url",
        style={'width': '97%', 'height': 40, 'background-color': '#212121', 'color': '#ffffff',
               'margin': '20px'},
    ),
    dbc.Button('Submit', id='url_textarea_button', n_clicks=0, outline=True,
               color='success', className="mr-1",
               style={'align': 'center', 'marginLeft': '20px'}),
    html.Div(id='url_textarea_output', style={
        'whiteSpace': 'pre-line', 'marginLeft': '20px'})
])


@app.callback(
    [Output('url_textarea_output', 'children'),
     Output('alert_div', 'children'),
     Output('memory', 'data')],
    [Input('url_textarea_button', 'n_clicks')],
    [State('url_textarea', 'value')]
)
def show_comments_df(n_clicks ,url):
    """Shows a dataframe of 100 comments from the input url.
        If the url is invalid, an alert is shown.
       A method written using callback decorator.
    Arguments:
        n_clicks {int} -- The count of the clicks.
        url {str} -- The input url as a string.

    Returns:
        list -- A list of graphical df, alert and data in json to session storage
        (All could be None).
    """
    if n_clicks > 0:

        if(url is None or url == ""):
            return [None, components.timed_alert("Please enter a URL and try again!", "danger", 4),
                    None]
        try:
            dataframe = backend.return_df_from_data(url)
            return [components.dark_table(dataframe, height='450px'),
                    None, dataframe.to_dict()]

        except error_utils.InvalidURLException as inv_url:
            error_msg = inv_url.args
            return [None, components.timed_alert(error_msg, "danger", 4), None]
        except api_err.HttpError:
            error_msg = "Invalid Youtube URL. The data could not be extracted."
            return [None, components.timed_alert(error_msg, "danger", 4), None]
        except Exception:
            error_msg = "An unknown error has occured. Please try again!"
            return [None, components.timed_alert(error_msg, "danger", 4), None]
