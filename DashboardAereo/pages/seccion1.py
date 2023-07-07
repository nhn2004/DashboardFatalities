import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from app import app


df = pd.read_csv('DashboardAereo/pages/aviation-accident-data-2023-05-16.csv')
fechas = df.date
dias = fechas.str.split("-", expand=True)[0]
df['day'] = dias

df['location'][df['location'].isnull()]='unknown'
df['operator'][df['operator'].isnull()]='unknown'
df['fatalities'][df['fatalities'].isnull()]='unknown'
df['registration'][df['registration'].isnull()]='unknown'
df['date'][df['date'].str.contains('unk')]='unknown'
df['type'][df['type'].str.contains('unknown')]='unknown'
df['country'][df['country'].str.contains('nkn')]='unknown'
df['country'][df['country'].str.contains('\?')]='unknown'
df['location'][df['location'].str.contains('\?')]='unknown'
df = df.replace(["??","date unk.","Unknown"], "unknown")

#Añadimos meses
lmonth=[]
for date in df['date']:
    if date.count('-')==2:
        mes=date.split('-')[1]
        lmonth.append(mes)
    else: 
        lmonth.append(date)

df['month']=lmonth
df['month'][df['month'].str.contains('\?')]='unknown'
df['month'][df['month'].str.contains('14')]='unknown'

dfnan = df.replace("unknown",np.nan)
dfnan.day = dfnan.day.astype(float)
dfnan.year = pd.to_datetime(dfnan.year).dt.year
dfnan

topfatalities = dfnan.sort_values('fatalities', ascending=False)
for ind, row in topfatalities.iterrows():
    if not str(row.fatalities).isnumeric() and type(row.fatalities) != float:
        topfatalities.fatalities.loc[ind] = int(row.fatalities.split("+ ")[0]) + int(row.fatalities.split("+ ")[1])

topfatalities.fatalities = topfatalities.fatalities.astype(dtype = "float")
topfatalities.year = topfatalities.year.astype(dtype = "float")

#TOP 10 FATAL FLIGHTS (DISASTERS)
top10fatal = topfatalities.sort_values("fatalities", ascending = False).head(10)

#GRAPHIC
figtop = px.bar(top10fatal,title = 'Los 10 vuelos con mayor número de decesos', y = 'registration', x = 'fatalities', orientation = "h", hover_name = "date",color = 'fatalities',color_continuous_scale='Inferno',hover_data=["type", "country"])

top10planes = df.groupby('type').count().sort_values('registration',ascending=False).head(10).reset_index()
#GRAPHIC
figtopplanes=px.bar(top10planes, x = 'registration', y = 'type', title = 'Los 10 modelos de aviones más involucrados en accidentes', orientation = 'h',color = 'registration',color_continuous_scale='Cividis_r')

operators = dfnan.groupby('operator').count().sort_values('date',ascending=False).reset_index()


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Introducción y datos principales", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        html.Div([
            dbc.Row([
                html.H3("Top 10 Vuelos con más Decesos")
            ]),
            dcc.Graph(figure= figtop, id="top-10-fatal")
        ]),
        html.Br(),
        html.Div([
            dbc.Row([
                html.H3("Top 10 Tipos de Aviones con más Accidentes")
            ]),
            dcc.Graph(figure=figtopplanes, id="top-10-planes")

        ])
        ,html.Div([
            dbc.Row([html.H3("Top 10 operadores (aerolíneas) con mayor número de accidentes")]),
            dbc.Row([
                #html.P("Seleccione: "),
                dcc.Checklist(
        id='checkbox',
        options=[{'label': ' Filtrar datos militares', 'value': 'option'}],
        value=[])
        ])
        ]), 
        html.Div([
            dcc.Graph('airline')
        ])
        

    ])
])

@app.callback(
    Output('airline', 'figure'),
    [Input('checkbox', 'value')]
)

def filterAF(value):
    if 'option' in value:
        f1 = operators[~operators['operator'].str.contains('AF')]
        f2 = f1[~f1['operator'].str.contains('Navy')]
        f3 = f2[~f2['operator'].str.contains('navy')]
        return px.bar(f3.head(10), orientation = 'h', y = 'operator',x = 'date',title= 'Los 10 operadores (aerolíneas con más accidentes)', color = 'date', color_continuous_scale = 'Aggrnyl')
    return px.bar(operators.head(10), orientation = 'h', y = 'operator',x = 'date',title= 'Los 10 operadores (aerolíneas con más accidentes)', color = 'date', color_continuous_scale = 'Aggrnyl') 


if __name__ == "__main__":
    app.run_server(debug=True)