import plotly.express as px
import pandas as pd

import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from app import app




image_urls = [
    'assets/avion-accidente1.jpg',
    'assets/avion-accidente2.jpg',
    'assets/avion-accidente1.jpg',
    'assets/avion-accidente2.jpg'
]
# change to app.layout if running as single page app instead
layout = html.Div([
    # dbc.Container([
        # dbc.Row([
        html.Div([
            html.H1("Vuelos Fatídicos", className="text-center"),
            html.H3("Desvelando los Trágicos Accidentes Aéreos", className="text-center")
        ], style={'position': 'relative','top': '50px'}),      
        # ]),
       

        # # dbc.Row([
        # #     dbc.Col(html.H5(children='It consists of two main pages: Global, which gives an overview of the COVID-19 cases and deaths around the world, '
        # #                              'Singapore, which gives an overview of the situation in Singapore after different measures have been implemented by the local government.')
        # #             , className="mb-5")
        # # ]),

        # # dbc.Row([
        # #     dbc.Col(dbc.Card(children=[html.H3(children='Get the original datasets used in this dashboard',
        # #                                        className="text-center"),
        # #                                dbc.Row([dbc.Col(dbc.Button("Global", href="https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863",
        # #                                                            color="primary"),
        # #                                                 className="mt-3"),
        # #                                         dbc.Col(dbc.Button("Singapore", href="https://data.world/hxchua/covid-19-singapore",
        # #                                                            color="primary"),
        # #                                                 className="mt-3")], justify="center")
        # #                                ],
        # #                      body=True, color="dark", outline=True)
        # #             , width=4, className="mb-4"),

        # #     dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
        # #                                        className="text-center"),
        # #                                dbc.Button("GitHub",
        # #                                           href="https://github.com/meredithwan/covid-dash-app",
        # #                                           color="primary",
        # #                                           className="mt-3"),
        # #                                ],
        # #                      body=True, color="dark", outline=True)
        # #             , width=4, className="mb-4"),

        # #     dbc.Col(dbc.Card(children=[html.H3(children='Read the Medium article detailing the process',
        # #                                        className="text-center"),
        # #                                dbc.Button("Medium",
        # #                                           href="https://medium.com/@meredithwan",
        # #                                           color="primary",
        # #                                           className="mt-3"),

        # #                                ],
        # #                      body=True, color="dark", outline=True)
        # #             , width=4, className="mb-4")
        # # ], className="mb-5"),

        # # html.A("Special thanks to Flaticon for the icon in COVID-19 Dash's logo.",
        # #        href="https://www.flaticon.com/free-icon/coronavirus_2913604")
        # # dbc.Row([
        # # html.Div(
        # #     children=[
        # #         html.H1('Slider de Imágenes'),
        # #         dcc.Slider(
        # #             id='slider',
        # #             min=0,
        # #             max=2,
        # #             step=1,
        # #             value=0,
        # #             marks={0: 'Imagen 1', 1: 'Imagen 2', 2: 'Imagen 3'}
        # #         ),
        # #         html.Div(id='slider-output2')
        # #     ]
        # # )
        # # ]),
         
        html.Img(src='assets/avion-home.png',style={'max-width': '100%', 'height': 'auto', 'margin-top':'15px'}),
                    
        
        
        html.H5(children=' 1970-2023: Una mirada aérea a los accidentes trágicos que han dejado su huella en la historia', className="text-center", style={'margin-top':'20px'})

           


    # ])

])





# @app.callback(
#     dash.dependencies.Output('slider-output2', 'children'),
#     [dash.dependencies.Input('slider', 'value')]
# )
# def update_slider_output(value):
#     if value == 0:
#         image_url = 'assets/avion-accidente1.jpg'
#     elif value == 1:
#         image_url = 'assets/avion-accidente2.jpg'
#     else:
#         image_url = 'assets/avion-accidente2.jpg'

#     return html.Img(src=image_url, style={'width': '100%'})

# @app.callback(
#     Output('slider-output', 'children'),
#     [Input('interval-component', 'n_intervals')]
# )
# def update_slider_output(n):
#     image_index = n % len(image_urls)
#     image_url = image_urls[image_index]
#     return html.Img(src=image_url, style={'width': '100%'})

