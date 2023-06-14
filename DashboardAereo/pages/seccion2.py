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
df = df.replace("??", "unknown")
df = df.replace("date unk.", "unknown")


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

#DASH SCROLLDOWNS
typeaccident = "H"
lossordamage = "1"
año = 2001
#FILTER
catdf = dfnan[dfnan.cat == typeaccident + lossordamage]

#GRAPHIC
px.histogram(catdf[catdf.year == año], x = 'month', title = 'Número de accidentes anuales por categoría',labels={
                     "count": "Número de accidentes",
                     "month": "Meses"
                 })

numfatbycat = topfatalities.groupby('cat').sum().reset_index()
numacc_bycat = topfatalities.groupby('cat').count().reset_index()

normdf = pd.concat([numacc_bycat.cat,numacc_bycat.registration,numfatbycat.fatalities], axis = 1)
normdf['fatality_rate']= (normdf.fatalities/normdf.registration)

#GRAPHIC (bar chart)
px.bar(normdf, x = 'cat', y = 'fatality_rate',title = "Tasa de fatalidad por categoria", labels={
                     "fatality_rate": "Tasa de fatalidad",
                     "cat": "Categorías"
                 })


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Causas comunes de accidentes", className="text-center")
                    , className="mb-5 mt-5")
        ]),
    ])
])