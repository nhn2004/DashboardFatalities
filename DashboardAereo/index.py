import plotly.express as px
import pandas as pd

import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from app import server
from app import app
from pages import  home, seccion1, seccion2, seccion3, seccion4, about

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
                    html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/titulo-blanco.png", height="60px"),style={"height":"6vw","margin-top":"5px"}),
                        
                    ],
                    align="center",
                    className="g-0",
                    
                ),
                href="/home",
                style={"display":"flex"}
                ),
                    dbc.Nav(
                    className="me-auto",
                    children=[
                        dbc.NavItem(
                            dbc.NavLink("Inicio", active=True, href="/home"),
                        ),
                        dbc.NavItem(
                            dbc.NavLink("Acerca del Proyecto", active=True, href="/about"),
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
                

                ])
                
            ],
            
        ),
    ]),
    color="primary",
    dark=True,
)


footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P("Este es el footer de la página.", className="text-center text-muted"),
            className="py-3"
        )
    ),
    fluid=True,
    className="bg-dark text-light",
    # style={"position": "fixed", "bottom": 0, "width": "100%"}
)
footer= dbc.Container(

        dbc.Container(
        [
            dbc.Row(
                    dbc.Nav(
                    className="me-auto",
                    children=[
                        dbc.NavItem(
                            dbc.NavLink("Privacidad", href="#",style={"color":"white","font-size":"12pt"})
                        ),
                        dbc.NavItem(
                            dbc.NavLink("|", href="#",style={"color":"white","font-size":"12pt"})
                        ),
                        dbc.NavItem(
                            dbc.NavLink("Accesibilidad", href="#",style={"color":"white","font-size":"12pt"}),
                        ),
                        dbc.NavItem(
                            dbc.NavLink("|", href="#",style={"color":"white","font-size":"12pt"})
                        ),
                        dbc.NavItem(
                            dbc.NavLink("Política de la Web", href="#",style={"color":"white","font-size":"12pt"}),
                        ),
                        dbc.NavItem(
                            dbc.NavLink("|", href="#",style={"color":"white","font-size":"12pt"})
                        ),
                        dbc.NavItem(
                            dbc.NavLink("Contáctanos", href="#",style={"color":"white","font-size":"12pt"}),
                        ),
                        
                    ],style={"display":"flex","justify-content":"center"}
                )
                    # html.Ul(
                    #     [
                    #         html.Li(html.A("Privacidad", href="/about/Pages/privacy.aspx", target="_blank"),className="item-footer"),
                    #         html.Li(html.A("Accesibilidad", href="/about/Pages/acessibility.aspx", target="_blank"),className="item-footer"),
                    #         html.Li(html.A("Politica de la Web", href="/about/Pages/Website-Policies.aspx", target="_blank"),className="item-footer"),
                            
                    #         html.Li(html.A("FOIA", href="/about/foia", target="_blank"),className="item-footer"),
                            
                    #         html.Li(html.A("Contactanos", href="/about/Pages/contact.aspx", target="_blank"),className="item-footer"),
                    #     ]
                    # ),
                    
                    # className="lista-horizontal",
                    
                
            ),
            html.Hr(style={"margin-top":"35px"}),
            dbc.Row(
                [
                    dbc.Col(
                        html.P(
                            [
                                html.Span("Investigacion sobre los accidentes quese han reportado desde 1961", className="mobile-break"),
                                
                            ]
                        ),
                        width=9
                    ),
                    dbc.Col(
                        html.P(
                            [
                                html.A("AIR (Aircraft Incident Report)", href="#", target="_blank",style={"color":"white"}),
                                
                            ]
                        ),
                        width=3,
                        className="right"
                    ),
                ],
                className="credits",
                style={"margin-top":"35px"}
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Container(
                        [
                            html.H4("Contactanos:",style={"color":"white"}),
                    #         dbc.Nav(
                    
                            dbc.Nav(
                                className="me-auto",
                                children=[
                                    
                                    
                                    html.A(html.Img(src="assets/social-midia-1.png", height="50px"), href="#"),
                                   
                                    html.A(html.Img(src="assets/social-midia-2.png", height="50px"), href="#"),
                                   
                                    html.A(html.Img(src="assets/social-midia-3.png", height="50px"), href="#"),
                                    # html.A(html.I(className="fab fa-flickr"), href="#", target="_blank"),
                                    # html.A(html.I(className="fab fa-linkedin"), href="#", target="_blank"),
                                ],
                                
                                
                            ),
                            
                        ],
                        
                        
                        ),
                        width=6,
                        className="social-media",
                        style={"display": "flex", "align-items": "center", "justify-content": "center"}
                    ),
                    dbc.Col(
                        html.Div(
                            html.Img(alt="NTSB Seal", src="assets/logo-imagen-avion.png", style={"height":"150px"}),
                            className="logo",
                            style={"display":"flex","justify-content":"center"}
                        ),
                        width=6
                    ),
                ],
                style={"margin-top":"15px"}
            ),
        ],
        
        className="container",
        
        
    ),
    fluid=True,
    className="bg-dark text-light",
    style={ "padding": "64px 0"}
    
    
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
    dbc.Col(style={"height":"4px","background-color":"#ce3434"}),
    html.Div(id='page-content'),
    dbc.Col(style={"height":"4px","background-color":"#ce3434","margin": "32px 0 0 0"}),
    footer,
    
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
    elif pathname == '/about':
        return about.layout
    
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)