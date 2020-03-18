import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import numpy as np
import pandas as pd
from dash.dependencies import State, Input, Output
from dash.exceptions import PreventUpdate
from app import app
import datetime
from datetime import datetime as dt
from datetime import date as dtoday
import os
import time
df = pd.read_csv("./data/AllCombinedData1.csv")
cert_columns =['Viscosity',
 'GelTime',
 'CureTime',
 'FinalCure',
 'ClassContent',
 ]
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
                                html.H3("Select a Defect"),
                                dcc.Dropdown(
                                    id="dropdown-select_defect",
                                    options= defect_options,
                                    value = 'Blisters'),
                                 
                            ],
                            className = 'box',
                            style = { "float":"left","width":"25em", "padding-right":'3em', "margin-top": '-4em'},
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
                                    start_date = dt(2019, 9, 18),
                                    end_date = dt(2020, 3, 5)
                                ),
                            ],    
                               
                            id="date-picker-outer",
                            className="box",
                            style = { "float":"left", "padding-left":"3em","width":"25em","margin-top": '-4em'},
                        ),
                        
                        html.Div(
                           
                            [
                                
                                html.H3("Submit Selections"),
                                html.Button(id = 'submit-button', n_clicks = 0, children ='Submit', 
                                style= {"width": "15em", 'height': '3em', "background-color": 'white'},
                                className = 'button1'),
                                
                            ],
                            
                            className="box button",
                            style = { "float":"left", "padding-left":"3em","width":"25em", "margin-top":"-4em"},
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
                            className = "box1",
                            children = dcc.Graph(id ="plot_1"),
                        ),
                        html.Div(
                            id = 'where_in_festoon',
                            className = "box2",
                            children = dcc.Graph(id = 'plot_2')
                        ),
                    ],
                ),
                html.Div(
                    id = 'last_row',
                    className = 'clearfix',
                    children = [
                        html.Div(
                            id = 'material_box_plot',
                            className = 'box3',
                            children = dcc.Graph(id = 'plot_3'),
                        ),
                        html.Div(
                            id = 'process_params_box_plot',
                            className = 'box4',
                            children = dcc.Graph(id = 'plot_4'),
                        ),
                    ],

                ),
            ],

        ),
    ],
    ),
]

@app.callback(
    Output("plot_1", "figure"),
    [Input('submit-button', 'n_clicks')],
    [State('dropdown-select_defect', 'value'),
     State("date-picker-range",'start_date'),
     State("date-picker-range", 'end_date')],
)
def plot_all_defects(n_clicks, value, start_date, end_date):
    if n_clicks == 0:
        df1 = df.dropna(subset = [value])
        df1 = df1[df1[value]!= 0]
       
        
    if n_clicks > 0:
        
        if start_date is None:
            start_date = dt(2019,9,18)    
        if end_date is None:
            end_date = dt(2020,3,5)
        df1 = df.dropna(subset = [value])
       
        df1 = df1[(df1['createdTime']>= start_date) & (df1["createdTime"]<= end_date)]
        df1 = df1[df1[value]!= 0]
   
    x= df1.groupby("partNumber").count()["Unnamed: 0"].index
    
    y = df1.groupby("partNumber").count()["Unnamed: 0"].values
    
    data = [go.Bar(x = x, y = y, marker_color = 'lightsalmon')]
    layout = go.Layout(xaxis = dict(type = "category"))
    fig = go.Figure(data = data, layout = layout)
    #fig = go.Figure(go.Bar(x=x, y=y, marker_color = 'lightsalmon'))
    fig.update_layout(title_text = value +" By Part", template = 'plotly_dark')

    return fig


@app.callback(
    Output("plot_2", "figure"),
    [Input('submit-button', 'n_clicks')],
    [State('dropdown-select_defect', 'value'),
     State("date-picker-range",'start_date'),
     State("date-picker-range", 'end_date')],
)
def plot_festoon_placement(n_clicks,value, start_date, end_date):
    if n_clicks == 0:
        df1 = df.dropna(subset = [value])
        df_defects = df1[df1[value]!= 0.0]
        print('hi')
        
    if n_clicks > 0:
        
        if start_date is None:
            start_date = dt(2019,9,18)    
        if end_date is None:
            end_date = dt(2020,3,5)
        df1 = df.dropna(subset = [value])
        df1 = df1[(df1['createdTime']>= start_date) & (df1["createdTime"]<= end_date)]
        df_defects = df1[df1[value]> 0]
    
    
    
    
    fig = go.Figure([go.Histogram(x = df_defects['percent'], marker_color = '#aaff44')])
    fig.update_layout(title_text = value + ' Placement in Festoon', template = "plotly_dark")
    return fig
    
    


@app.callback(
    Output("plot_3", "figure"),
    [Input('submit-button', 'n_clicks')],
    [State('dropdown-select_defect', 'value'),
     State("date-picker-range",'start_date'),
     State("date-picker-range", 'end_date')],
)
def plot_material_box(n_clicks,value, start_date, end_date):
    ## need the parts in the picker to by dynamic to the info
    ## or send back no data for that time
    if n_clicks == 0:
        df1 = df.dropna(subset = [value])
        df_cert = df1[df1[value]!= 0.0]
        
    if n_clicks > 0:
        
        if start_date is None:
            start_date = dt(2019,9,18)    
        if end_date is None:
            end_date = dt(2020,3,5)
        df1 = df.dropna(subset = [value])
       
        df1 = df1[(df1['createdTime']>= start_date) & (df1["createdTime"]<= end_date)]
        df_cert = df1[df1[value]> 0]
    
    
    
    fig = go.Figure()
    y0 = df_cert[cert_columns[0]]
    
    y1 = df_cert[cert_columns[1]]
    y2 = df_cert[cert_columns[2]]
    y3 = df_cert[cert_columns[3]]
    y4 = df_cert[cert_columns[4]]
   
    fig.add_trace(go.Box(y=y0, name = cert_columns[0], marker_color = '#f23844'))
    fig.add_trace(go.Box(y=y1, name = cert_columns[1], marker_color = '#c0ff21'))
    fig.add_trace(go.Box(y=y2, name = cert_columns[2], marker_color = '#21fffb'))
    fig.add_trace(go.Box(y=y3, name = cert_columns[3], marker_color = '#eb46cc'))
    fig.add_trace(go.Box(y=y4, name = cert_columns[4], marker_color = 'lightsalmon'))
    
    fig.update_layout(title_text= "Material Deviations for "+ value, template = "plotly_dark")
    
    return fig

@app.callback(
    Output("plot_4", "figure"),
    [Input('submit-button', 'n_clicks')],
    [State('dropdown-select_defect', 'value'),
     State("date-picker-range",'start_date'),
     State("date-picker-range", 'end_date')],
)
def plot_process_params_box(n_clicks,value, start_date, end_date):
    ## need the parts in the picker to by dynamic to the info
    ## or send back no data for that time
    if n_clicks == 0:
        df1 = df.dropna(subset = [value])
        df_defects = df1[df1[value]!= 0.0]
        
    if n_clicks > 0:
        
        if start_date is None:
            start_date = dt(2019,9,18)    
        if end_date is None:
            end_date = dt(2020,3,5)
        df1 = df.dropna(subset = [value])
       
        df1 = df1[(df1['createdTime']>= start_date) & (df1["createdTime"]<= end_date)]
        df_defects = df1[df1[value]> 0]
    
    colors = [ '#eb46cc', 'lightsalmon', '#aaff44']
   
    df_shifts1 = df_defects[df_defects["Shift"]==1].count()[0]
    df_shifts2 = df_defects[df_defects["Shift"]==2].count()[0]
    df_shifts3 = df_defects[df_defects["Shift"]==3].count()[0]
    labels = ["FirstShift", "SecondShift", "ThirdShift"]
    
    values = [df_shifts1, df_shifts2, df_shifts3]
    fig = go.Figure([go.Pie(labels = labels, values = values)])
    fig.update_traces(hoverinfo = "label+percent", textinfo = "value", textfont_size = 20, 
                       marker = dict(colors = colors, line = dict(color = '#222222', width = 1)))
    fig.update_layout(title_text="Shift with the Most " + value, template= "plotly_dark")
    return fig
