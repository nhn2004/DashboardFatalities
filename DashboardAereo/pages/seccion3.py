import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots


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

Acc=html.Div([
            dbc.Row([
                dbc.Col([
                    html.P('Decades:')
                    ,dcc.Dropdown(
                     options=decades, id='decadesDropdown', value="20's"
                    )
                    ,html.Br()
                    ,dcc.Graph(id='linechart')
                    ,html.P('Years:')
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
        total.sort_values(by='year', inplace=True, ascending=True)
        total.sort_values(by='month', key=lambda x: pd.Categorical(x, categories=monthsSorted, ordered=True),inplace=True )
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
            yaxis_title='N. of fatalities',
            xaxis_title = None
            ,title= 'Fatilities Count per Month'
            , grid_columns = 1, grid_rows = 2)
        a=-1
        list_colors=['blue','red','orange','white'] #Los colores los pone Nahin
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
                header = dict(values=['MEAN',' MEDIAN']),
                cells =  dict(values=[[round(total['fatalities'].mean(),2)],[total['fatalities'].median()]]))
                    
        fig.add_trace(table, row = 2, col = 1)
        table.domain=dict(x=[0, 0.5], y=[0.01, 0.01])
        
        fig2=px.bar(data_frame=total , x='month',y='fatalities',hover_name='year',color='year',text=total['percentage'], height=899, width=900)
        for value,month in zip(totalFatXyear,total['month'].unique()):
            value=int(value)
            fig2.add_annotation(x=month,y=value+0.1*value,text=f'total:{value}', font={'size':12 ,'color':'blue'}, textangle=0,showarrow=False,align='center',opacity=1)
        fig2.update_layout(autosize=False, width=1100,
            yaxis_title='N. of fatalities',
            xaxis_title = 'Months',
            title= 'Fatalities Count per Month')
        fig2.update_traces(textfont_color='white')    
        
    elif b2==True:
        for y in range(y_start,y_finish+1):
            y=str(y)
            YearsChoseByUser.append(gb_year_month[gb_year_month['year']==y])
        
        total=pd.concat(YearsChoseByUser)
        total.sort_values(by='year', inplace=True, ascending=True)
        total.sort_values(by='month', key=lambda x: pd.Categorical(x, categories=monthsSorted, ordered=True),inplace=True )
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
            yaxis_title='N. of accidents',
            xaxis_title = None
            ,title= 'Accidents Count per Month'
            , grid_columns = 1, grid_rows = 2)
        a=-1
        list_colors=['blue','red','orange','white'] #Los colores los pone Nahin
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
        fig2.update_layout(autosize=False, width=1100,
            yaxis_title='N. of accidents',
            xaxis_title = 'Months',
            title= 'Accidents Count per Month')
        fig2.update_traces(textfont_color='white')       
    
    return fig,fig2

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