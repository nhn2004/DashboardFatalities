import plotly.express as px
import pandas as pd

import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from app import app

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Introducción y datos principales", className="text-center")
                    , className="mb-5 mt-5")
        ]),
    ])
])