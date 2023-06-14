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
            dbc.Col(html.H1("Explora más", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Img(src="assets/avion-accidente1.jpg", style={'height':'230px','border-radius': '30px'})
                ],style={"display":"flex","justify-content":"center"}),
                dbc.Col([
                    html.P("Descubre una visión visual impactante de las estadísticas de decesos aéreos ocurridos desde 1970 en todo el mundo. Nuestro dashboard te brinda la funcionalidad de explorar y analizar los datos detallados de los accidentes trágicos, centrándonos especialmente en los modelos de aviones, aerolíneas y otros factores relacionados.",
                           style={'font-size':'1.4em'})
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.P("Identifica los patrones y tendencias más alarmantes, así como los elementos que se consideran de mayor riesgo debido a su historial de problemas. Aprovecha esta herramienta intuitiva para obtener información valiosa sobre la seguridad aérea y tomar decisiones más informadas en tus viajes.",
                           style={'font-size':'1.4em'})
                ], style={'text-align':'right'}),
                
                dbc.Col([
                    html.Img(src="assets/avion-accidente2.jpg", style={'height':'230px','border-radius': '30px'})
                ],style={"display":"flex","justify-content":"center"}),
            ], style={'margin-top':'30px'})
        ]),
        html.Div([
            dbc.Row([
                html.H1("Colaboradores" , className="text-center")
            ], style={'margin-top':'50px'}),
            html.Div([
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Img(src="assets/Nahin.jpg", style={'height':'300px','width': '300px','object-fit': 'cover','border-radius': '50%','overflow': 'hidden'})
                        ],style={"display":"flex","justify-content":"center"}),
                        html.Div([
                            html.H3(["Cevallos Vinces",
                                    html.Br(),
                                    "Nahin Jussephe"
                            ], style={'text-align':'center'}),
                            html.P(["Estudiante de Ingenieria",
                                    html.Br(),
                                    "Mecatrónica (Espol)"], style={'text-align':'center'})

                        ],style={"margin-top":"20px"})
                    
                    ])
                ]),
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Img(src="assets/Jorge2.jpg", style={'height':'300px','width': '300px','object-fit': 'cover','border-radius': '50%','overflow': 'hidden'})
                        ],style={"display":"flex","justify-content":"center"}),
                        html.Div([
                            html.H3(["Apolo Acosta",
                                    html.Br(),
                                    "Jorge Alberto"
                            ], style={'text-align':'center'}),
                            html.P(["Estudiante de Ingenieria",
                                    html.Br(),
                                    "Mecatrónica (Espol)"], style={'text-align':'center'})

                        ],style={"margin-top":"20px"})
                    
                    ])
                ]),
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Img(src="assets/David.jpg", style={'height':'300px','width': '300px','object-fit': 'cover','border-radius': '50%','overflow': 'hidden'})
                        ],style={"display":"flex","justify-content":"center"}),
                        html.Div([
                            html.H3(["Sumba Correa",
                                    html.Br(),
                                    "David Salomón"
                            ], style={'text-align':'center'}),
                            html.P(["Estudiante de Ingenieria",
                                    html.Br(),
                                    "Computación (Espol)"], style={'text-align':'center'})

                        ],style={"margin-top":"20px"})
                    
                    ])
                ])
            ], style={'display':'flex','flex-direction':'row','margin-top':'30px'})
        ])
    ])
])