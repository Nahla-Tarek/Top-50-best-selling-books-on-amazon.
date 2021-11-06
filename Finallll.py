# -*- coding: utf-8 -*-
import dash
from dash import html 
from dash import dcc
import plotly.express as px
from dash.dependencies import Input,Output,State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd

df= pd.read_csv("bestsellers with categories.csv")

app= dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout=html.Div([ 
    dbc.Row(
        [
            dbc.Col(html.Img(src=app.get_asset_url('Amazon_logo.png'), 
                             style={'height':'60%', 'width':'50%','margin-left': '5vh', 'margin-top': '5vh'}),
                    width=5,lg=2),
            
            dbc.Col(html.Img(src=app.get_asset_url('vertical-line.png'), 
                             style={'height':'60%', 'width':'20%', 'margin-top': '5vh'}),
                    width=2,lg=1),
            
            dbc.Col(html.H1("Top 50 Best Selling Books",
                            style={'textAlign': 'left', 'fontSize': 25, 'margin-top': '5vh'}), width=20, lg=3)
        ]
        ),
    
    dbc.Row(dbc.Col(html.H3("Genre",
                            style={'textAlign': 'left', 'margin-left': '5vh','margin-top': '7vh', 'fontSize': 15}))),
            
    dbc.Row(
        dbc.Col(
            dcc.Checklist(
                id='checklist',
                options=[
                    {'label': k, 'value': k, 'disabled':False} for k in df['Genre'].unique()],
                style={'width': '20%', 'display': 'inline-block','margin-left': '5vh'}), width=5)),
    dbc.Row(
        dbc.Col(
            dcc.Slider(
                id='year--slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].max(),
                marks={str(year): str(year) for year in df['Year'].unique()}), width=8)),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='figure_slider',
                          style={'width': '150vh', 'height': '70vh','display': 'inline-block',
                                 'background-color':'grey'}), width=9),
            dbc.Col(
                dbc.Row(
                    [
                    dbc.Card(
                        dbc.CardBody([
                        html.H5("Author", className="card-title"),                      
                        html.Div([
                            html.Div(
                            id="textarea-output",
                            style={'textAlign': 'center','color': 'darkblue','font-size': 18}),
                        ])
                        ])),
                    dbc.Card(
                        dbc.CardBody([
                        html.H5("Price", className="card-title"),                      
                        html.Div([
                            html.Div(
                            id="textarea-output1",
                            style={'textAlign': 'center','color': 'darkblue','font-size': 18})
                        ])
                        ]),style={'margin-top': '3vh'}),                       
                        ]
                    
        ), style={'textAlign': 'center',"width": "3rem", 'margin-top': '15vh','margin-right': '3vh'})
        ])
 ])  

@app.callback(
    Output(component_id='figure_slider', component_property="figure"),
    [Input(component_id='year--slider', component_property="value")],
    [Input(component_id='checklist', component_property="value")])

def update_figure(select_year, value_chosen):
    if value_chosen == None or len(value_chosen)== 0:
        filter= df[df.Year==select_year]
        data1=[
            go.Bar(x=filter['Name'], y=filter['Reviews'],yaxis='y1', name='Reviews',opacity=0.9),
            go.Scatter(x=filter['Name'], y=filter['User Rating'],line=dict(color="darkorange"), yaxis='y2',
                       name='User Rating')]
        
        y1 = go.YAxis(title='Reviews', titlefont=go.Font(color='blue'))
        y2 = go.YAxis(title= 'User Rating', titlefont=go.Font(color='darkorange'))
        y2.update(overlaying='y', side='right')
        layout = go.Layout(yaxis1 = y1, yaxis2 = y2)
        fig1 = go.Figure(data=data1, layout=layout)
        fig1.update_layout(
         xaxis = {
         'tickmode': 'array',
         'tickvals': list(range(0,filter.shape[0],1)),
         'ticktext': filter['Name'].str.slice(-10).tolist(),
         "tickangle":90})
               
    else:
        filter= df[(df.Year==select_year) & (df.Genre.isin(value_chosen))]
        print(value_chosen)
        data1=[
            go.Bar(x=filter['Name'], y=filter['Reviews'], yaxis='y1', name='Reviews',opacity=0.9),
            go.Scatter(x=filter['Name'], y=filter['User Rating'],line=dict(color="darkorange"),
                       yaxis='y2', name='User Rating')]      
        y1 = go.YAxis(title='Reviews', titlefont=go.Font(color='blue'))
        y2 = go.YAxis(title= 'User Rating', titlefont=go.Font(color='darkorange'))
        y2.update(overlaying='y', side='right')
        layout = go.Layout(yaxis1 = y1, yaxis2 = y2)
        fig1 = go.Figure(data=data1, layout=layout)

        fig1.update_layout(
         xaxis = {
         'tickmode': 'array',
         'tickvals': list(range(0,filter.shape[0],1)),
         'ticktext': filter['Name'].str.slice(-15).tolist(),
         "tickangle":90})
        
    fig1.update_layout(
        transition_duration=800,
        legend=dict(
            orientation="h",
            y=1.1,
            x=1,
            yanchor="top",
            xanchor="right"))
    return fig1

@app.callback(
        Output('textarea-output', 'children'),
        Output('textarea-output1', 'children'),
        Input("figure_slider", "clickData"))
    
def update_auther(clickdata):
    book_name = clickdata['points'][0]['x']
    auther = df[df['Name']== book_name]['Author'].unique()
    price = df[df['Name']== book_name]['Price'].unique()
    print(f'Price of the Book : {price}')
    print(f'Author of the Book : {auther}')
    return str(auther[0]),str(price[0])+' $'     

app.run_server(threaded=True)