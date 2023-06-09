import plotly.express as px
import pandas as pd

import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from app import server
from app import app
from pages import  home, seccion1, seccion2, seccion3, seccion4

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        # dbc.DropdownMenuItem("Inicio", href="/home"),
        dbc.DropdownMenuItem("Introducción y datos principales", href="/seccion1"),
        dbc.DropdownMenuItem("Causas comunes de accidentes", href="/seccion2"),
        dbc.DropdownMenuItem("Patrones geográficos y temporales", href="/seccion3"),
        dbc.DropdownMenuItem("Modelos de aviones involucrados", href="/seccion4"),
    ],
    nav = True,
    in_navbar = True,
    label = "Secciones",
    style={
                                                "data-bs-toggle": "dropdown",
                                                
                                                "role": "button",
                                                "aria-haspopup": "true",
                                                "aria-expanded": "false",
                                            },
)



navbar = dbc.Navbar(
    dbc.Container([
        # html.A(
        #         # Use row and col to control vertical alignment of logo / brand
        #         dbc.Row(
        #             [
        #                 dbc.Col(html.Img(src="assets/logo_espol.png", height="30px"),style={"position": "relative", "right": "1vw"}),
        #                 dbc.Col(dbc.NavbarBrand("ESPOL DASH", className="ml-2")),
        #             ],
        #             align="center",
        #             className="g-0"
        #         ),
        #         href="/home",
        #     ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            id="navbar-collapse",
            navbar=True,
            children=[
                dbc.Container([
                    dbc.Nav(
                    className="me-auto",
                    children=[
                        dbc.NavItem(
                            dbc.NavLink("Inicio", active=True, href="/home"),
                        ),
                        dbc.NavItem(
                            dbc.NavLink("Acerca del Proyecto", href="#"),
                        ),
                        # dbc.NavItem(
                        #     dbc.NavLink("Pricing", href="#"),
                        # ),
                        # dbc.NavItem(
                        #     dbc.NavLink("About", href="#"),
                        # ),
                        dbc.NavItem(
                            
                                children=dropdown
                            
                        ),
                    ],
                ),
                html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/logo_espol.png", height="30px"),style={"position": "relative", "right": "1vw"}),
                        dbc.Col(dbc.NavbarBrand("ESPOL DASH", className="ml-2")),
                    ],
                    align="center",
                    className="g-0",
                    
                ),
                href="/home",
                style={"display":"flex"}
                )

                ])
                
            ],
            
        ),
    ]),
    color="primary",
    dark=True,
)





# navbar = dbc.Navbar(
#     dbc.Container(
#         [
            # html.A(
            #     # Use row and col to control vertical alignment of logo / brand
            #     dbc.Row(
            #         [
            #             dbc.Col(html.Img(src="assets/logo_espol.png", height="30px"),style={"position": "relative", "right": "1vw"}),
            #             dbc.Col(dbc.NavbarBrand("ESPOL DASH", className="ml-2")),
            #         ],
            #         align="center",
            #         className="g-0"
            #     ),
            #     href="/home",
            # ),
#             dbc.NavbarToggler(id="navbar-toggler2"),
#             dbc.Collapse(
#                 dbc.Nav(
#                     # right align dropdown menu with ml-auto className
#                     [dropdown], className="ml-auto", navbar=True
#                 ),
#                 id="navbar-collapse2",
#                 navbar=True,
#             ),
#         ]
#     ),
#     # color="dark",
#     dark=True,
#     className="mb-4",
# )

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/seccion1':
        return seccion1.layout
    elif pathname == '/seccion2':
        return seccion2.layout
    elif pathname == '/seccion3':
        return seccion3.layout
    elif pathname == '/seccion4':
        return seccion4.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)