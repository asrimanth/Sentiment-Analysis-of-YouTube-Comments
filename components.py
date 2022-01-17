import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc


def timed_alert(message, status, time_in_sec):
    """Returns a timed alert dbc component to the user, which can be shown in a div.

    Arguments:
        message {str} -- A message to be shown in the alert.
        status {str} -- The nature of the alert. Takes the following values:
                        primary, secondary, success, warning, danger, info, light and dark.
        time_in_sec {int} -- The time duration for which the alert should stay alive.

    Returns:
        {dbc.Alert obj} -- An alert message object which must be shown in an html.Div object.
    """
    return dbc.Alert(
                message,
                id="alert-auto",
                is_open=True,
                color=status,
                duration=time_in_sec * 1000,
            ),


def dark_table(dataframe, width='1420px', height='600px'):
    return html.Div(children=[
        dash_table.DataTable(
            data=dataframe.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in dataframe.columns],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_cell={
                'textAlign': 'left',
                'backgroundColor': '#212121',
                'textColor': 'white',
                'minWidth': '50px', 'maxWidth': '250px',
            },
            style_table={
                'maxHeight': height,
                'maxWidth' : width,
                'overflowX': 'scroll',
                'overflowY': 'scroll',
            },
            style_cell_conditional=[
                {'if': {'column_id': 'user_id'},
                'textAlign':'center', 'width': '220px'},
                {'if': {'column_id': 'likes'},
                'width': '50px'},
            ]
        ),
    ],style={'whiteSpace': 'pre-line', 'marginLeft': '20px'})


def dark_table_result(dataframe, width='1420px', height='600px'):
    return html.Div(children=[
        dash_table.DataTable(
            data=dataframe.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in dataframe.columns],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_cell={
                'textAlign': 'left',
                'backgroundColor': '#212121',
                'textColor': 'white',
                'minWidth': '50px', 'maxWidth': '250px',
            },
            style_table={
                'maxHeight': height,
                'maxWidth' : width,
                'overflowX': 'scroll',
                'overflowY': 'scroll',
            },
            style_cell_conditional=[
                {'if': {'column_id': 'user_id'},
                'textAlign':'center', 'width': '220px'},
                {'if': {'column_id': 'likes'},
                'width': '50px'},
            ],
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{sentiment_value} > 0.3',
                    },
                    'backgroundColor': 'forestgreen',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{sentiment_value} < -0.3',
                    },
                    'backgroundColor': 'tomato',
                    'color': 'white'
                },
            ]
        ),
    ],style={'whiteSpace': 'pre-line', 'marginLeft': '20px'})

def dbc_table(dataframe):
    dbc.Table.from_dataframe(dataframe, striped=True, bordered=True, hover=True,
        size= 'sm',
        style={
            'height': '500px',
            'width' : '40px',
            'overflow-x': 'scroll',
            'overflow-y': 'scroll'}
        ),
