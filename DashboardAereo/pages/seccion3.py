import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import folium
import json
import requests
from fuzzywuzzy import fuzz,process

import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from app import app

# %% [markdown]
# # Aviation Accidents (1919 to 2020)

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import plotly.graph_objects as go


# %%
df = pd.read_csv('DashboardAereo/pages/aviation-accident-data-2023-05-16.csv')
# df
df['location'][df['location'].isnull()]='unknown'
df['operator'][df['operator'].isnull()]='unknown'
df['fatalities'][df['fatalities'].isnull()]='unknown'
df['registration'][df['registration'].isnull()]='unknown'


# %%
df[df['year'].str.contains('\?')].groupby('year').count()

# %%
df['date'][df['date'].str.contains('unk')]='unknown'
df['type'][df['type'].str.contains('unknown')]='unknown'
df['country'][df['country'].str.contains('nkn')]='unknown'
df['country'][df['country'].str.contains('\?')]='unknown'
df['location'][df['location'].str.contains('\?')]='unknown'



# %%
#columna month

l=[]

for date in df['date']:
    if date.count('-')==2:
        mes=date.split('-')[1]
        l.append(mes)
    else: l.append(date)
        
df['month']=l
df['month'][df['month'].str.contains('\?')]='unknown'
df['month'][df['month'].str.contains('14')]='unknown'

# %% [markdown]
# date - Date of the accident
# 
# type - Type of aircraft
# 
# registration - Registration of the aircraft
# 
# operator - Operator of the aircraft
# 
# fatalities - Number of fatalities
# 
# location - Location of the accident
# 
# country - Country of the accident
# 
# cat - Category of the accident described by ASN
# 
# year - Year of the accident

# %%
# df

# %% [markdown]
# En que meses del año han ocurrido más accidentes aéreos?
# 
# paises en mapa en el que muestre total accidentes/decesos
# 
# año de más accidentes, typo más famoso por año
# 
# existe correlación entre la categoria de vuelo y los accidentes
# 
# MAPA: Nuevo dataset de población por paises desde 1920 por decadas
# etc

# %%

# df.info()

# %%

# df.month.unique()

# %% [markdown]
# DataFrame "df" was copied into dfnan with np.nan instead of "unknowns".

# %%

dfnan = df.replace("unknown",np.nan)
# dfnan.head()

# %%

# dfnan.info()

# %% [markdown]
# 
# ## Turning fatalities into numbers

# %%

topfatalities = dfnan.sort_values('fatalities', ascending=False)
topfatalities.fatalities.unique()

# %%
for ind, row in topfatalities.iterrows():
    if not str(row.fatalities).isnumeric() and type(row.fatalities) != float:
        topfatalities.fatalities.loc[ind] = int(row.fatalities.split("+ ")[0]) + int(row.fatalities.split("+ ")[1])

# %%
topfatalities.fatalities = topfatalities.fatalities.astype(dtype = "float")

# %%

#topfatalities.fatalities[topfatalities.fatalities.apply(type) == str]

# %% [markdown]
# 
# We get the flight accidents with the most casualties. We get to see that the deadliest flights were the 9/11 attacks at New York, USA in 2001.

# %%
topfatalities.sort_values("fatalities", ascending = False)

# %% [markdown]
# ## Checking unique registers

# %%
df[df.duplicated()]

# %%
df[df.registration == 'NT+NL']

# %% [markdown]
# Let's drop the duplicates.

# %%
df.drop_duplicates(subset = 'registration')
df[df.registration == 'NT+NL']

# %%
df[df.duplicated()]

# %% [markdown]
# ## Managing dates (month and year)

# %% [markdown]
# Checking amount of NaNs in both date, month, and year columns.

# %%

# dfnan.info()

# %% [markdown]
# Transforming years to float because of cardinality benefits.

# %%
dfnan.year = pd.to_datetime(dfnan.year).dt.year


# %%

gb_year_month=topfatalities.groupby(['year','month']).agg({'fatalities':'sum','cat':'count'})
gb_year_month.reset_index(level='month',inplace=True)
gb_year_month.reset_index(level='year',inplace=True)

#YearsChoseByUser.append(p)
#YearsChoseByUser.append(o)



#total=pd.concat(YearsChoseByUser) #USED IN CALLBACK
def sum_columnXyear(df,column,monthsSorted):
    AllYearsFatalities={month: 0 for month in monthsSorted}
    for month in df['month'].unique():
        value=df[column][df['month']==month].sum()
        AllYearsFatalities[month]+=value
    return list(AllYearsFatalities.values())
monthsSorted= ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
#total.sort_values(by='year', inplace=True, ascending=True)
#total.sort_values(by='month', key=lambda x: pd.Categorical(x, categories=monthsSorted, ordered=True),inplace=True )



# %%
#totalFatXyear=sum_columnXyear(total,'fatalities')

# %%

#s=total.groupby('month')['fatalities'].transform('sum')
#total['sumXmonth']=s
#total['percentage']=(total['fatalities']/total['sumXmonth']*100).map('{:.1f}%'.format)



# %%
#helpful to dash: https://plotly.com/python/line-charts/
'''fig= px.line(total, x='month', y='fatalities', hover_name='year', color='year', markers=True)
fig.update_traces(line=dict(dash='dash'),)

for val,tipo in zip([total['fatalities'].max(),total['fatalities'].min()],['max','min']):
    month=total['month'][total['fatalities']==val].values[0]
    if tipo=='min':
        val=val-20
    else: val=val+20
    fig.add_annotation(x=month, y=val, text=f'{tipo.upper()}',align='center',showarrow=False)

table=go.Table(
        header = dict(values=['MEAN',' MEDIAN']),
        cells =  dict(values=[[total['fatalities'].mean()],[total['fatalities'].median()]])
            )
             
table.domain=dict(x=[0.0001, 0.25], y=[0.99, 0.99])
fig.add_trace(table)
## fig 2
fig=px.bar(data_frame=total , x='month',y='fatalities',hover_name='year',color='year',text=total['percentage'], height=899, width=900)
for value,month in zip(totalFatXyear,total['month'].unique()):
    value=int(value)
    fig.add_annotation(x=month,y=value+25,text=f'total:{value}', font={'size':12 ,'color':'blue'}, textangle=0,showarrow=False,align='center',opacity=1)
fig.update_layout(autosize=False, width=950)
fig.update_traces(textfont_color='white')'''

df_coordinates=pd.read_csv('DashboardAereo\pages\coordinates.csv')
df_coordinates.dropna(inplace=True)

countries_geometries= 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson'
response = requests.get(countries_geometries)
data= json.loads(response.text)

admin_names = [feature['properties']['ADMIN'] for feature in data["features"]]
geometries= [feature['geometry']['coordinates'] for feature in data["features"]]
coor=[]

country_dict = {
    "Afganistán": "Afghanistan",
    "Albania": "Albania",
    "Alemania": "Germany",
    "Andorra": "Andorra",
    "Angola": "Angola",
    "Antigua y Barbuda": "Antigua and Barbuda",
    "Arabia Saudita": "Saudi Arabia",
    "Argelia": "Algeria",
    "Argentina": "Argentina",
    "Armenia": "Armenia",
    "Aruba": "Aruba",
    "Australia": "Australia",
    "Austria": "Austria",
    "Azerbaiyán": "Azerbaijan",
    "Bahamas": "Bahamas",
    "Bangladés": "Bangladesh",
    "Barbados": "Barbados",
    "Baréin": "Bahrain",
    "Bélgica": "Belgium",
    "Belice": "Belize",
    "Benín": "Benin",
    "Bielorrusia": "Belarus",
    "Birmania": "Myanmar",
    "Bolivia": "Bolivia",
    "Bosnia y Herzegovina": "Bosnia and Herzegovina",
    "Botsuana": "Botswana",
    "Brasil": "Brazil",
    "Brunéi": "Brunei",
    "Bulgaria": "Bulgaria",
    "Burkina Faso": "Burkina Faso",
    "Burundi": "Burundi",
    "Bután": "Bhutan",
    "Cabo Verde": "Cape Verde",
    "Camboya": "Cambodia",
    "Camerún": "Cameroon",
    "Canadá": "Canada",
    "Catar": "Qatar",
    "Chad": "Chad",
    "Chile": "Chile",
    "China": "China",
    "Chipre": "Cyprus",
    "Ciudad del Vaticano": "Vatican City",
    "Colombia": "Colombia",
    "Comoras": "Comoros",
    "Corea del Norte": "North Korea",
    "Corea del Sur": "South Korea",
    "Costa de Marfil": "Ivory Coast",
    "Costa Rica": "Costa Rica",
    "Croacia": "Croatia",
    "Cuba": "Cuba",
    "Dinamarca": "Denmark",
    "Dominica": "Dominica",
    "Ecuador": "Ecuador",
    "Egipto": "Egypt",
    "El Salvador": "El Salvador",
    "Emiratos Árabes Unidos": "United Arab Emirates",
    "Eritrea": "Eritrea",
    "Eslovaquia": "Slovakia",
    "Eslovenia": "Slovenia",
    "España": "Spain",
    "Estados Unidos de America": "United States of America",
    "Estonia": "Estonia",
    "Etiopía": "Ethiopia",
    "Fiji": "Fiji",
    "Filipinas": "Philippines",
    "Finlandia": "Finland",
    "Francia": "France",
    "Gabón": "Gabon",
    "Gambia": "Gambia",
    "Georgia": "Georgia",
    "Ghana": "Ghana",
    "Granada": "Grenada",
    "Grecia": "Greece",
    "Guatemala": "Guatemala",
    "Guinea": "Guinea",
    "Guinea-Bisáu": "Guinea-Bissau",
    "Guinea Ecuatorial": "Equatorial Guinea",
    "Guyana": "Guyana",
    "Haití": "Haiti",
    "Honduras": "Honduras",
    "Hungría": "Hungary",
    "India": "India",
    "Indonesia": "Indonesia",
    "Irak": "Iraq",
    "Irán": "Iran",
    "Irlanda": "Ireland",
    "Islandia": "Iceland",
    "Islas Marshall": "Marshall Islands",
    "Islas Salomón": "Solomon Islands",
    "Israel": "Israel",
    "Italia": "Italy",
    "Jamaica": "Jamaica",
    "Japón": "Japan",
    "Jordania": "Jordan",
    "Kazajistán": "Kazakhstan",
    "Kenia": "Kenya",
    "Kirguistán": "Kyrgyzstan",
    "Kiribati": "Kiribati",
    "Kuwait": "Kuwait",
    "Laos": "Laos",
    "Lesoto": "Lesotho",
    "Letonia": "Latvia",
    "Líbano": "Lebanon",
    "Liberia": "Liberia",
    "Libia": "Libya",
    "Liechtenstein": "Liechtenstein",
    "Lituania": "Lithuania",
    "Luxemburgo": "Luxembourg",
    "Madagascar": "Madagascar",
    "Malasia": "Malaysia",
    "Malaui": "Malawi",
    "Maldivas": "Maldives",
    "Malí": "Mali",
    "Malta": "Malta",
    "Marruecos": "Morocco",
    "Mauricio": "Mauritius",
    "Mauritania": "Mauritania",
    "México": "Mexico",
    "Micronesia": "Micronesia",
    "Moldavia": "Moldova",
    "Mónaco": "Monaco",
    "Mongolia": "Mongolia",
    "Montenegro": "Montenegro",
    "Mozambique": "Mozambique",
    "Namibia": "Namibia",
    "Nauru": "Nauru",
    "Nepal": "Nepal",
    "Nicaragua": "Nicaragua",
    "Níger": "Niger",
    "Nigeria": "Nigeria",
    "Noruega": "Norway",
    "Nueva Zelanda": "New Zealand",
    "Omán": "Oman",
    "Países Bajos": "Netherlands",
    "Pakistán": "Pakistan",
    "Palaos": "Palau",
    "Panamá": "Panama",
    "Papúa Nueva Guinea": "Papua New Guinea",
    "Paraguay": "Paraguay",
    "Perú": "Peru",
    "Polonia": "Poland",
    "Portugal": "Portugal",
    "Reino Unido": "United Kingdom",
    "República Centroafricana": "Central African Republic",
    "República Checa": "Czech Republic",
    "República del Congo": "Republic of the Congo",
    "República Democrática del Congo": "Democratic Republic of the Congo",
    "República Dominicana": "Dominican Republic",
    "Ruanda": "Rwanda",
    "Rumania": "Romania",
    "Rusia": "Russia",
    "Samoa": "Samoa",
    "San Cristóbal y Nieves": "Saint Kitts and Nevis",
    "San Marino": "San Marino",
    "San Vicente y las Granadinas": "Saint Vincent and the Grenadines",
    "Santa Lucía": "Saint Lucia",
    "Santo Tomé y Príncipe": "Sao Tome and Principe",
    "Senegal": "Senegal",
    "Serbia": "Serbia",
    "Seychelles": "Seychelles",
    "Sierra Leona": "Sierra Leone",
    "Singapur": "Singapore",
    "Siria": "Syria",
    "Somalia": "Somalia",
    "Sri Lanka": "Sri Lanka",
    "Suazilandia": "Eswatini",
    "Sudáfrica": "South Africa",
    "Sudán": "Sudan",
    "Sudán del Sur": "South Sudan",
    "Suecia": "Sweden",
    "Suiza": "Switzerland",
    "Surinam": "Suriname",
    "Tailandia": "Thailand",
    "Tanzania": "Tanzania",
    "Tayikistán": "Tajikistan",
    "Timor Oriental": "East Timor",
    "Togo": "Togo",
    "Tonga": "Tonga",
    "Trinidad y Tobago": "Trinidad and Tobago",
    "Túnez": "Tunisia",
    "Turkmenistán": "Turkmenistan",
    "Turquía": "Turkey",
    "Tuvalu": "Tuvalu",
    "Ucrania": "Ukraine",
    "Uganda": "Uganda",
    "Uruguay": "Uruguay",
    "Uzbekistán": "Uzbekistan",
    "Vanuatu": "Vanuatu",
    "Venezuela": "Venezuela",
    "Vietnam": "Vietnam",
    "Yemen": "Yemen",
    "Yibuti": "Djibouti",
    "Zambia": "Zambia",
    "Zimbabue": "Zimbabwe"
}
######
######
######
######
######
######
button = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Button("Conteo de fallecimientos por accidente", color="primary", id='b1',n_clicks=1, value='1'), width="auto"),
                dbc.Col(dbc.Button("Conteo de casos de accidente",color="secondary", id='b2',n_clicks=0, value='2'), width="auto"),
            ],
            justify="center",
            align="center",
        )
    ],
    className="d-grid gap-2 col-6 mx-auto",
)

decades=[
    {'label':"70's", 'value':"70's"},
    { 'label':"80's",'value':"80's"},
    { 'label':"90's",'value':"90's"},
    { 'label':"00's",'value':"00's"},
    { 'label':"10's",'value':"10's"},
    { 'label':"20's",'value':"20's"}
]

type_input= html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Input(id='input_country',
                      placeholder='Escriba un país (en español)...'
                    , type='text'
                                  )
            )
        
    ])
    , html.Br()
    , dbc.Row([dbc.Col(
            id='map'
        )])
  
])

stations={'Primavera':['MAR','APR','MAY'],'Verano':['JUN','JUL','AUG'],'Otoño':['OCT','SEP','NOV'],'Invierno':['DEC','JAN','FEB']}
map_countries=html.Div([
    dbc.Row([
        dbc.Col(
            [dbc.Switch(
                    id="swPr",
                    label='Primavera',
                    value=False,)
                ,dcc.Checklist(id='checklistPr',options= stations['Primavera'],value=[])]
            )
        ,dbc.Col([
            dbc.Switch(
                    id="swVe",
                    label='Verano',
                    value=False)
                ,dcc.Checklist(id='checklistVe',options= stations['Verano'],value=[])
            ])
        ,dbc.Col([
            dbc.Switch(
                    id="swOt",
                    label='Otoño',
                    value=False)
                ,dcc.Checklist(id='checklistOt',options= stations["Otoño"],value=[])
            ])
        ,dbc.Col([
            dbc.Switch(
                    id="swIn",
                    label='Invierno',
                    value=False)
                ,dcc.Checklist(id='checklistIn',options= stations['Invierno'],value=[])
            ])   
])])

Acc=html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Décadas:')
                    ,dcc.Dropdown(
                     options=decades, id='decadesDropdown', value="20's"
                    )
                    ,html.Br()
                    ,dcc.Graph(id='linechart')
                    ,html.P('Años:')
                    ,dcc.RangeSlider(
                        id='range-slider',
                        min=1970,
                        max=2023,
                        step=1,
                        marks={year: str(year) for year in range(1970, 2024, 10)},
                        value=[2020, 2023]
                        )
                    ,html.Br()
                    ,dcc.Graph(id='barchart')  ])])
                    ,html.Br()
                    ,type_input
                    ,html.Br()
                    ,map_countries
                    
                    
        ])

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Patrones geográficos y temporales", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        button
        , html.Div(id='button_selected')
    
  ])
])
@app.callback(
    Output('b1','color'),
    Output('b2','color'),
    Output('b1','disabled'),
    Output('b2','disabled'),
    Output('button_selected','children'),
    Input('b1','n_clicks'),
    Input('b2','n_clicks'),
    State("b1", "disabled"), 
    State("b2", "disabled")  
)
def update_button_colors(clicks_button1, clicks_button2,bd1,bd2):
    
    if clicks_button1 > clicks_button2:
        bd1=True 
        bd2=False
        return "primary", "secondary",bd1,bd2,Acc
    elif clicks_button2 <= clicks_button1:
        bd2=True
        bd1=False
        return "secondary", "primary",bd1,bd2,Acc
    else:
        bd1,bd2=False,False
        return  "primary", "secondary",bd1,bd2,Acc

@app.callback(
    Output('range-slider', 'min'),
    Output('range-slider', 'max'),
    Output('range-slider', 'value'),
    Output('range-slider', 'marks'),
    Input('decadesDropdown', 'value')
)
def update_range_slider(value):
    
    for dec in ["70's","80's","90's","00's","10's","20's"]:
        if (value==dec):
            if (dec!="20's"):
                year_start= int(dec.replace("'s",""))
                century=1900
                if year_start in [0,10]:
                    century=2000
                year_start+=century
                year_finish=year_start+9
                
                
            else:
                year_start=2020
                year_finish=2023
                
                

            min= year_start; max=year_finish; rang=[year_start,year_start+3]
            marks={year: str(year) for year in range(year_start, year_finish+1)}
            return min,max,rang,marks

@app.callback(
    Output('linechart','figure'),
    Output('barchart','figure'),
    Input('range-slider','value'),
    State("b1", "disabled"), 
    State("b2", "disabled")

    
) 
def update_linechart(range_s,b1,b2):
    y_start, y_finish= range_s
    YearsChoseByUser=[]
    if b1==True:
        for y in range(y_start,y_finish+1):
            y=str(y)
            YearsChoseByUser.append(gb_year_month[gb_year_month['year']==y])
        
        total=pd.concat(YearsChoseByUser)
        #total.sort_values(by='year', inplace=True, ascending=True)
        #total.sort_values(by='month', key=lambda x: pd.Categorical(x, categories=monthsSorted, ordered=True),inplace=True )
        total.sort_values(by=['year', 'month'], ascending=[True, True], inplace=True, key=lambda x: pd.Categorical(x, categories=monthsSorted, ordered=True))
        totalFatXyear=sum_columnXyear(total,'fatalities',monthsSorted)    
        s=total.groupby('month')['fatalities'].transform('sum')
        total['sumXmonth']=s
        total['percentage']=(total['fatalities']/total['sumXmonth']*100).map('{:.1f}%'.format)
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.80, 0.20],
            specs=[[{"type": "xy"}],[{"type": "table"}]])

        fig.update_traces(line=dict(dash='dash'),)
        fig.update_layout(
            yaxis_title='Número de decesos',
            xaxis_title = None
            ,title= 'Número de decesos por meses'
            , grid_columns = 1, grid_rows = 2)
        a=-1
        list_colors=['blue','red','green','violet','orange','lightblue','pink','lightgreen','brown','yellow'] 
        for y in np.sort(total.year.unique()):
            a+=1
            
            fig.add_trace(go.Scatter(x = total[total.year == y].month, y=total[total.year == y].fatalities, showlegend = True, 
            mode = 'lines+markers', 
            #marker_color = int(y),
            line_color=list_colors[a],
            name = y,
            ),row=1, col=1)

        for val,tipo in zip([total['fatalities'].max(),total['fatalities'].min()],['max','min']):
            month=total['month'][total['fatalities']==val].values[0]
            if tipo=='min':
                val=val-20
            else: val=val+20
            fig.add_annotation(x=month, y=val, text=f'{tipo.upper()}',align='center',showarrow=False)

        table = go.Table(
                header = dict(values=['MEDIA',' MEDIANA']),
                cells =  dict(values=[[round(total['fatalities'].mean(),2)],[total['fatalities'].median()]]))
                    
        fig.add_trace(table, row = 2, col = 1)
        table.domain=dict(x=[0, 0.5], y=[0.01, 0.01])
        
        fig2=px.bar(data_frame=total , x='month',y='fatalities',hover_name='year',color='year',text=total['percentage'], height=899, width=900)
        for value,month in zip(totalFatXyear,total['month'].unique()):
            value=int(value)
            fig2.add_annotation(x=month,y=value+0.1*value,text=f'total:{value}', font={'size':12 ,'color':'blue'}, textangle=0,showarrow=False,align='center',opacity=1)
        fig2.update_layout(autosize=False, width=1100,
            yaxis_title='Número de decesos',
            xaxis_title = 'Meses',
            title= 'Decesos por mes')
        fig2.update_traces(textfont_color='white')    
        
    elif b2==True:
        for y in range(y_start,y_finish+1):
            y=str(y)
            YearsChoseByUser.append(gb_year_month[gb_year_month['year']==y])
        
        total=pd.concat(YearsChoseByUser)
        #total.sort_values(by='year', inplace=True, ascending=True)
        #total.sort_values(by='month', key=lambda x: pd.Categorical(x, categories=monthsSorted, ordered=True),inplace=True )
        total.sort_values(by=['year', 'month'], ascending=[True, True], inplace=True, key=lambda x: pd.Categorical(x, categories=monthsSorted, ordered=True))
        AllYearsAccidents={month: 0 for month in monthsSorted}
        for month in total['month'].unique():
            value=total['cat'][total['month']==month].sum()
            AllYearsAccidents[month]+=value
        totalAccXyear=list(AllYearsAccidents.values())  
        s=total.groupby('month')['cat'].transform('sum')
        total['sumXmonth']=s
        total['percentage']=(total['cat']/total['sumXmonth']*100).map('{:.1f}%'.format)
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.80, 0.20],
            specs=[[{"type": "xy"}],[{"type": "table"}]])

        fig.update_traces(line=dict(dash='dash'),)
        fig.update_layout(
            yaxis_title='Número de accidentes',
            xaxis_title = None
            ,title= 'Número de accidentes por meses'
            , grid_columns = 1, grid_rows = 2)
        a=-1
        list_colors=['blue','red','green','violet','orange','lightblue','pink','lightgreen','brown','yellow'] 
        for y in np.sort(total.year.unique()):
            a+=1
            
            fig.add_trace(go.Scatter(x = total[total.year == y].month, y=total[total.year == y].cat, showlegend = True, 
            mode = 'lines+markers', 
            #marker_color = int(y),
            line_color=list_colors[a],
            name = y,
            ),row=1, col=1)

        for val,tipo in zip([total['cat'].max(),total['cat'].min()],['max','min']):
            month=total['month'][total['cat']==val].values[0]
            if tipo=='min':
                val=val-2
            else: val=val+2
            fig.add_annotation(x=month, y=val, text=f'{tipo.upper()}',align='center',showarrow=False)

        table = go.Table(
                header = dict(values=['MEDIA',' MEDIANA']),
                cells =  dict(values=[[round(total['cat'].mean(),2)],[total['cat'].median()]]))
                    
        fig.add_trace(table, row = 2, col = 1)
        table.domain=dict(x=[0, 0.5], y=[0.01, 0.01])
        
        total['sumXmonth']=s
        total['percentage']=(total['cat']/total['sumXmonth']*100).map('{:.1f}%'.format)
        
        fig2=px.bar(data_frame=total , x='month',y='cat',hover_name='year',color='year',text=total['percentage'], height=899, width=900)
        for value,month in zip(totalAccXyear,total['month'].unique()):
            value=int(value)
            fig2.add_annotation(x=month,y=value+2.5,text=f'total:{value}', font={'size':12 ,'color':'blue'}, textangle=0,showarrow=False,align='center',opacity=1)
        fig2.update_layout(autosize=False, width=1100,
            yaxis_title='Número de accidents',
            xaxis_title = 'Meses',
            title= 'Número de accidentes por mes')
        fig2.update_traces(textfont_color='white')       
    
    return fig,fig2



'''@app.callback(
    Output('map','children'),
    Input('decadesDropdown', 'value')
)

def show_map(value):
    for dec in ["70's","80's","90's","00's","10's","20's"]:
        if (value==dec):
            if (dec!="20's"):
                year_start= int(dec.replace("'s",""))
                century=1900
                if year_start in [0,10]:
                    century=2000
                year_start+=century
                year_finish=year_start+9              
            else:
                year_start=2020
                year_finish=2023
            m=folium.Map()
            for lat,lon,fat,loc in zip( df_coordinates.Latitude[df_coordinates['year'].between(year_start,year_finish)], df_coordinates.Longitude[df_coordinates['year'].between(year_start,year_finish)], df_coordinates.fatalities[df_coordinates['year'].between(year_start,year_finish)], df_coordinates.location[df_coordinates['year'].between(year_start,year_finish)] ):
                if fat==0:
                    plane_icon_url ='Bplane.png'
                    folium.Marker(
                    [lat,lon], popup=f'<i>{loc}</i>',icon=folium.CustomIcon(plane_icon_url, icon_size=(20, 20))).add_to(m)
                else:
                    plane_icon_url= 'Yplane.png'
                    folium.Marker(
                    [lat,lon], popup=f'<i>{loc}</i> \n \n <b>Descesos:{int(fat)}</b>',icon=folium.CustomIcon(plane_icon_url, icon_size=(20, 20))).add_to(m)
            m_html= m.get_root().render()
            return html.Iframe(srcDoc=m_html, width="100%", height=500)'''
@app.callback(
    Output("checklistPr", "style"),
    Output("checklistVe", "style"),
    Output("checklistOt", "style"),
    Output("checklistIn", "style"),
    Input("swPr", "value"),
    Input("swVe", "value"),
    Input("swOt", "value"),
    Input("swIn", "value")
)
def toggle_checklist(on_pr, on_ve, on_ot, on_in):
    checklist_styles = [{"display": "none"}] * 4
    if on_pr:
        checklist_styles[0] = {"display": "block"}
    if on_ve:
        checklist_styles[1] = {"display": "block"}
    if on_ot:
        checklist_styles[2] = {"display": "block"}
    if on_in:
        checklist_styles[3] = {"display": "block"}
    return checklist_styles  
                        
@app.callback(
    Output('map','children'),
    Input('decadesDropdown', 'value'),
    Input('input_country','n_submit'),
    State('input_country','value')
    
)

def zoomin_country(value_dr,enter,value_in):
    for dec in ["70's","80's","90's","00's","10's","20's"]:
        if (value_dr==dec):
            if (dec!="20's"):
                year_start= int(dec.replace("'s",""))
                century=1900
                if year_start in [0,10]:
                    century=2000
                year_start+=century
                year_finish=year_start+9              
            else:
                year_start=2020
                year_finish=2023
            m=folium.Map()
            for lat,lon,fat,loc,year,month in zip( df_coordinates.Latitude[df_coordinates['year'].between(year_start,year_finish)], df_coordinates.Longitude[df_coordinates['year'].between(year_start,year_finish)], df_coordinates.fatalities[df_coordinates['year'].between(year_start,year_finish)], df_coordinates.location[df_coordinates['year'].between(year_start,year_finish)],df_coordinates.year[df_coordinates['year'].between(year_start,year_finish)], df_coordinates.month[df_coordinates['year'].between(year_start,year_finish)] ):
                if fat==0:
                    plane_icon_url ='DashboardAereo\pages\Bplane.png'
                    folium.Marker(
                    [lat,lon], popup=f'<i>{loc}</i>\n\nAño-Mes:\n<b>{int(year)}-{month}</b>',icon=folium.CustomIcon(plane_icon_url, icon_size=(20, 20))).add_to(m)
                else:
                    plane_icon_url= 'DashboardAereo\pages\Yplane.png'
                    folium.Marker(
                    [lat,lon], popup=f'<i>{loc}</i>\n\nDescesos:<b>{int(fat)}</b>\nAño-Mes:<b>\n{int(year)}-{month}</b> ',icon=folium.CustomIcon(plane_icon_url, icon_size=(20, 20))).add_to(m)
    if enter is not None:
        fzcountry,fzscore=process.extractOne(value_in, country_dict.keys(), scorer=fuzz.ratio)
        for name,bound in zip(admin_names,geometries):
            if name==country_dict[fzcountry]:
                coor=[]
                for boun in bound:
                    for cor in boun:
                        for c in cor:
                            cor_ordered=[c[1],c[0]]
                            coor.append(tuple(cor_ordered))
                m.fit_bounds(coor)
                break
        enter=None
    m_html= m.get_root().render()
    return html.Iframe(srcDoc=m_html, width="100%", height=500)

if __name__ == "__main__":
    app.run_server(debug=True)


'''            
@app.callback(
    Output('b1','color'),
    Output('b2','color'),
    Output('b1','disabled'),
    Output('b2','disabled'),
    Output('linechart','figure'),
    Output('barchart','figure'),
    Output('button_selected','children'),
    Input('b1','n_clicks'),
    Input('b2','n_clicks'),
    Input('range-slider','value'),
    State("b1", "disabled"), 
    State("b2", "disabled")  
)
def update_button_colorsNshowgraphs(clicks_button1, clicks_button2, range_s, bd1, bd2):
    y_start, y_finish= range_s
    YearsChoseByUser=[]
    if clicks_button1 > clicks_button2:
        bd1=True 
        bd2=False
        for y in range(y_start,y_finish+1):
            y=str(y)
            YearsChoseByUser.append(gb_year_month[gb_year_month['year']==y])
        
        total=pd.concat(YearsChoseByUser)
        total.sort_values(by='year', inplace=True, ascending=True)
        total.sort_values(by='month', key=lambda x: pd.Categorical(x, categories=monthsSorted, ordered=True),inplace=True )
        totalFatXyear=sum_columnXyear(total,'fatalities',monthsSorted)    
        s=total.groupby('month')['fatalities'].transform('sum')
        total['sumXmonth']=s
        total['percentage']=(total['fatalities']/total['sumXmonth']*100).map('{:.1f}%'.format)
        
        fig= px.line(total, x='month', y='fatalities', hover_name='year', color='year', markers=True)
        fig.update_traces(line=dict(dash='dash'),)

        for val,tipo in zip([total['fatalities'].max(),total['fatalities'].min()],['max','min']):
            month=total['month'][total['fatalities']==val].values[0]
            if tipo=='min':
                val=val-9
            else: val=val+9
            fig.add_annotation(x=month, y=val, text=f'{tipo.upper()}',align='center',showarrow=False)

        table=go.Table(
                header = dict(values=['MEAN',' MEDIAN']),
                cells =  dict(values=[[round(total['fatalities'].mean(),2)],[total['fatalities'].median()]])
                    )
                    
        table.domain=dict(x=[0.0001, 0.25], y=[0.99, 0.99])
        fig.add_trace(table)
        
        fig2=px.bar(data_frame=total , x='month',y='fatalities',hover_name='year',color='year',text=total['percentage'], height=899, width=900)
        for value,month in zip(totalFatXyear,total['month'].unique()):
            value=int(value)
            fig2.add_annotation(x=month,y=value+0.1*value,text=f'total:{value}', font={'size':12 ,'color':'blue'}, textangle=0,showarrow=False,align='center',opacity=1)
        fig2.update_layout(autosize=False, width=950)
        fig2.update_traces(textfont_color='white')    

        
        return "primary", "secondary",bd1,bd2,fig,fig2,Fatalities
    elif clicks_button2 <= clicks_button1:
        bd2=True
        bd1=False
        AllYearsAccidents={month: 0 for month in monthsSorted}
        for month in total['month'].unique():
            value=total['cat'][total['month']==month].sum()
            AllYearsAccidents[month]+=value
        totalAccXyear=list(AllYearsAccidents.values())  
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.80, 0.20],
            specs=[[{"type": "xy"}],[{"type": "table"}]])

        fig.update_traces(line=dict(dash='dash'),)
        fig.update_layout(
            yaxis_title='N. of accidents',
            xaxis_title = 'Months'
            ,title= 'Accidents Count per Month'
            , grid_columns = 1, grid_rows = 2)

        for y in np.sort(total.year.unique()):
            fig.add_trace(go.Scatter(x = total[total.year == y].month, y=total[total.year == y].cat, showlegend = True, 
            mode = 'lines+markers', 
            marker_color = int(y),
            name = y,
            ),row=1, col=1)

        for val,tipo in zip([total['cat'].max(),total['cat'].min()],['max','min']):
            month=total['month'][total['cat']==val].values[0]
            if tipo=='min':
                val=val-2
            else: val=val+2
            fig.add_annotation(x=month, y=val, text=f'{tipo.upper()}',align='center',showarrow=False)

        table = go.Table(
                header = dict(values=['MEAN',' MEDIAN']),
                cells =  dict(values=[[round(total['cat'].mean(),2)],[total['cat'].median()]]))
                    
        fig.add_trace(table, row = 2, col = 1)
        table.domain=dict(x=[0, 0.5], y=[0.01, 0.01])
        total['sumXmonth']=s
        total['percentage']=(total['cat']/total['sumXmonth']*100).map('{:.1f}%'.format)
        
        fig2=px.bar(data_frame=total , x='month',y='cat',hover_name='year',color='year',text=total['percentage'], height=899, width=900)
        for value,month in zip(totalAccXyear,total['month'].unique()):
            value=int(value)
            fig2.add_annotation(x=month,y=value+2.5,text=f'total:{value}', font={'size':12 ,'color':'blue'}, textangle=0,showarrow=False,align='center',opacity=1)
        fig2.update_layout(autosize=False, width=950)
        fig2.update_traces(textfont_color='white')      
        
        return "secondary", "primary",bd1,bd2,fig,fig2,Fatalities
    else:
        bd1,bd2=False,False
        for y in range(y_start,y_finish+1):
            y=str(y)
            YearsChoseByUser.append(gb_year_month[gb_year_month['year']==y])
        
        total=pd.concat(YearsChoseByUser)
        total.sort_values(by='year', inplace=True, ascending=True)
        total.sort_values(by='month', key=lambda x: pd.Categorical(x, categories=monthsSorted, ordered=True),inplace=True )
        totalFatXyear=sum_columnXyear(total,'fatalities',monthsSorted)    
        s=total.groupby('month')['fatalities'].transform('sum')
        total['sumXmonth']=s
        total['percentage']=(total['fatalities']/total['sumXmonth']*100).map('{:.1f}%'.format)
        
        fig= px.line(total, x='month', y='fatalities', hover_name='year', color='year', markers=True)
        fig.update_traces(line=dict(dash='dash'),)

        for val,tipo in zip([total['fatalities'].max(),total['fatalities'].min()],['max','min']):
            month=total['month'][total['fatalities']==val].values[0]
            if tipo=='min':
                val=val-9
            else: val=val+9
            fig.add_annotation(x=month, y=val, text=f'{tipo.upper()}',align='center',showarrow=False)

        table=go.Table(
                header = dict(values=['MEAN',' MEDIAN']),
                cells =  dict(values=[[round(total['fatalities'].mean(),2)],[total['fatalities'].median()]])
                    )
                    
        table.domain=dict(x=[0.0001, 0.25], y=[0.99, 0.99])
        fig.add_trace(table)
        
        fig2=px.bar(data_frame=total , x='month',y='fatalities',hover_name='year',color='year',text=total['percentage'], height=899, width=900)
        for value,month in zip(totalFatXyear,total['month'].unique()):
            value=int(value)
            fig2.add_annotation(x=month,y=value+0.1*value,text=f'total:{value}', font={'size':12 ,'color':'blue'}, textangle=0,showarrow=False,align='center',opacity=1)
        fig2.update_layout(autosize=False, width=950)
        fig2.update_traces(textfont_color='white')    
        
        
        return  "primary", "secondary",bd1,bd2,html.P('click:'),html.P('clcik_'),Fatalities
    
'''