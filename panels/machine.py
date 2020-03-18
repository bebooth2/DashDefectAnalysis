import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from app import app
import numpy as np
import pandas as pd
from dash.dependencies import State, Input, Output
from dash.exceptions import PreventUpdate

import datetime
from datetime import datetime as dt
from datetime import date as dtoday
import os
import time

df = pd.read_csv("./data/AllCombinedData1.csv")
defects = ['Cracks',
 'Dry Mix',
 'Blisters',
 'Molded in Flash',
 'Improper Sanding',
 'Non-Fills',
 'Chips',
 'Pits',
 'IMC Short Shots',
 'IMC Blisters',
 'Test Parts',
 'Press/Equip Malfunction',
 'Wavy',
 'IMC Peel',
 'IMC Chips',
 'Teardown',
 'IMC Tracks',
 'External Trials',
 'Holes Off',
 'Dips',
 'Paint Sags/Drips',
 'Poor Repair',
 'Too Heavy']
defect_options =[]
for x in defects:
    defect_options.append({"label": x, "value":x})
layout = [
    html.Div(

    children=[
        html.Div(
       
            children= [
                html.Div(
                    id="dropdown-select-outer",
                   className="clearfix",
                    children=[
                        html.Div(
                            [
                                html.H3("Select a Part"),
                                dcc.Dropdown(
                                    id="dropdown-select_3d",
                                    options= defect_options,
                                    value = 'Blisters'),
                                 
                            ],
                            className = 'box',
                            style = { "float":"left","width":"25em", "padding-right":'3em'},
                        ),
                       
                        html.Div(
                           
                            [
                                
                                html.H3("Select Date Range"),
                                dcc.DatePickerRange(
                                    id="date-picker-range",
                                    min_date_allowed=dt(2008, 1, 1),
                                    max_date_allowed=dtoday.today(), 
                                    initial_visible_month=dt(2019, 9, 1),
                                    display_format="MMM Do, YY",
                                ),
                            ],
                            id="date-picker-outer",
                            className="box",
                            style = { "float":"left", "padding-left":"3em","width":"25em"},
                        ),
                    ], 
                ),
                 html.Div(id='dataOutPut', style={'display': 'none'}),
              
                html.Div(
                    id="middle_row_graphs",
                    className = 'clearfix',
                    children = [
                        html.Div(
                            id= "parts_defect_counts",
                            className = "box_3d1",
                            children = dcc.Graph(id ="plot3d"),
                        ),],
                        ),
                html.Div(
                    id="middle_row_graphs",
                    className = 'clearfix',
                    children = [
                        html.Div(
                            id= "parts_defect_counts",
                            className = "box_3d2",
                            children = dcc.Graph(id ="plot3d2"),
                        ),],
                        ),
            ],



),],),]








@app.callback(
    Output("plot3d", "figure"),
    [Input("dropdown-select_3d", "value")],
)
def plot_process_params_box(value):
    ## need the parts in the picker to by dynamic to the info
    ## or send back no data for that time
    df1 = df.dropna(subset = [value])
    df_defects = df1[df1[value]!= 0.0]
    x = df_defects['percent']
    y = df_defects["Viscosity"]
    z = df_defects["ClassContent"]
    fig = go.Figure(data=[go.Scatter3d(x=x,y=y,z=z, mode = "markers", marker_color = 'hotpink')])
    fig.update_layout(template = "plotly_dark")
    return fig

@app.callback(
    Output("plot3d2", "figure"),
    [Input("dropdown-select_3d", "value")],
)
def plot_process_params_box2(value):
    ## need the parts in the picker to by dynamic to the info
    ## or send back no data for that time
    df1 = df.dropna(subset = [value])
    df_defects = df1[df1[value]>= 2]
    x = df_defects['percent']
    y = df_defects["Viscosity"]
    z = df_defects["ClassContent"]
    fig = go.Figure(data=[go.Scatter3d(x=x,y=y,z=z, mode = "markers", marker_color ='purple')])
    fig.update_layout(template = "plotly_dark")
    return fig