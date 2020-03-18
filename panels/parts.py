import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from graphPrograms import apuTracker_final as apu
from graphPrograms import df_by_press_or_parts as dpp
#from graphPrograms import defects_placement_final2 as dfp
from graphPrograms import pivot_by_part as pbp


import numpy as np
import pandas as pd
from dash.dependencies import State, Input, Output
#from dash.exceptions import PreventUpdate

import datetime
from datetime import datetime as dt
from datetime import date as dtoday
import os
import time
from app import app
# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
#app.config.suppress_callback_exceptions = True


# df_5 = pd.read_csv("./data/part_defect_counts.csv")
# choices = list(df_5["Part #"].values)
# parts_options = []
# for x in choices:
#     parts_options.append({"label":x, 'value':x})
df = pd.read_csv("./data/AllCombinedData1.csv")
part_choices = list(df["partNumber"].unique())
parts_options = []
for x in part_choices:
    parts_options.append({"label": x, "value":x})

cert_columns =['Viscosity',
 'GelTime',
 'CureTime',
 'FinalCure',
 'ClassContent',
 'ProductWeight',
 'ShrinkFactor',
 'SpecificGravity']


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
                                    id="dropdown-select",
                                    options= parts_options,
                                    value = '118439'),
                                 
                            ],
                            className = 'box',
                            style = { "float":"left","width":"25em", "padding-right":'3em',"margin-top": '-4em'},
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
                            children = dcc.Graph(id ="defect_counts"),
                        ),
                        html.Div(
                            id = 'where_in_festoon',
                            className = "box2",
                            children = dcc.Graph(id = 'festoon_placement')
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
                            children = dcc.Graph(id = 'material_box'),
                        ),
                        html.Div(
                            id = 'process_params_box_plot',
                            className = 'box4',
                            children = dcc.Graph(id = 'process_box'),
                        ),
                    ],

                ),
            ],

        ),
    ],
    ),
]
    


@app.callback(
    Output("defect_counts", "figure"),
    [Input('submit-button', 'n_clicks')],
    [State('dropdown-select', 'value'),
     State("date-picker-range",'start_date'),
     State("date-picker-range", 'end_date')]
)
def plot_all_defects(n_clicks,value, start_date, end_date):
    if n_clicks == 0:
        df1 = df[df['partNumber']==value]
        
    if n_clicks > 0:
        
        if start_date is None:
            start_date = dt(2019,9,18)    
        if end_date is None:
            end_date = dt(2020,3,5)
        
       
        df1 = df[(df['createdTime']>= start_date) & (df["createdTime"]<= end_date)]
        df1 = df1[df1['partNumber']==value]

    
    x = defects
    y = df1[defects].sum()[1:].values
    # x = list(df_5.columns)[1:]
    # y= df_5[df_5["Part #"] == value].values[0][1:]
    fig = go.Figure([go.Bar(x=x, y=y, marker_color ='#21fffb')])
    fig.update_layout(title_text = "Defect Counts", template = 'plotly_dark')

    return fig


@app.callback(
    Output("festoon_placement", "figure"),
    [Input('submit-button', 'n_clicks')],
    [State('dropdown-select', 'value'),
     State("date-picker-range",'start_date'),
     State("date-picker-range", 'end_date')],
)
def plot_festoon_placement(n_clicks,value, start_date, end_date):
    if n_clicks == 0:
        df1 = df[df['partNumber']==value]
        
    if n_clicks > 0:
        
        if start_date is None:
            start_date = dt(2019,9,18)    
        if end_date is None:
            end_date = dt(2020,3,5)
        
       
        df1 = df[(df['createdTime']>= start_date) & (df["createdTime"]<= end_date)]
        df1 = df1[df1['partNumber']==value]
    
    df_defects = df1.dropna(subset = defects)
    
    fig = go.Figure([go.Histogram(x = df_defects['percent'], marker_color = '#ff9900')])
    fig.update_layout(title_text = 'Defects Placement in Festoon', template = "plotly_dark")
    return fig
    


@app.callback(
    Output("material_box", "figure"),
    [Input('submit-button', 'n_clicks')],
    [State('dropdown-select', 'value'),
     State("date-picker-range",'start_date'),
     State("date-picker-range", 'end_date')],
)
def plot_material_box(n_clicks,value, start_date, end_date):
    ## need the parts in the picker to by dynamic to the info
    ## or send back no data for that time
    if n_clicks == 0:
        df1 = df[df["partNumber"]== value]
        
    if n_clicks > 0:
        
        if start_date is None:
            start_date = dt(2019,9,18)    
        if end_date is None:
            end_date = dt(2020,3,5)
        
       
        df1 = df[(df['createdTime']>= start_date) & (df["createdTime"]<= end_date)]
        df1 = df1[df1['partNumber']==value]
    
    df_cert = df1.dropna(subset=cert_columns)
    fig = go.Figure()
    y0 = df_cert[cert_columns[0]]
    
    y1 = df_cert[cert_columns[1]]
    y2 = df_cert[cert_columns[2]]
    y3 = df_cert[cert_columns[3]]
    y4 = df_cert[cert_columns[4]]
    y5 = df_cert[cert_columns[5]]
    y6 = df_cert[cert_columns[6]]
    y7 = df_cert[cert_columns[7]]
    fig.add_trace(go.Box(y=y0, name = cert_columns[0], marker_color = '#f23844'))
    fig.add_trace(go.Box(y=y1, name = cert_columns[1], marker_color = '#c0ff21'))
    fig.add_trace(go.Box(y=y2, name = cert_columns[2], marker_color = '#21fffb'))
    fig.add_trace(go.Box(y=y3, name = cert_columns[3], marker_color = '#eb46cc'))
    fig.add_trace(go.Box(y=y4, name = cert_columns[4], marker_color = '#ff8921'))
    #fig.add_trace(go.Box(y=y5, name = cert_columns[5], marker_color = '#bb1199'))
   # fig.add_trace(go.Box(y=y6, name = cert_columns[6], marker_color = '#ff9900'))
   # fig.add_trace(go.Box(y=y7, name = cert_columns[7], marker_color = '#a1b3c6'))
    fig.update_layout(title_text= "Material Deviations", template = "plotly_dark")
    
    return fig

@app.callback(
    Output("process_box", "figure"),
    [Input('submit-button', 'n_clicks')],
    [State('dropdown-select', 'value'),
     State("date-picker-range",'start_date'),
     State("date-picker-range", 'end_date')],
)
def plot_process_params_box(n_clicks,value, start_date, end_date):
    ## need the parts in the picker to by dynamic to the info
    ## or send back no data for that time
    if n_clicks == 0:
        df1 = df[df['partNumber']== value ]
        
    if n_clicks > 0:
        
        if start_date is None:
            start_date = dt(2019,9,18)    
        if end_date is None:
            end_date = dt(2020,3,5)
        
       
        df1 = df[(df['createdTime']>= start_date) & (df["createdTime"]<= end_date)]
        df1 = df1[df1['partNumber']==value]
    colors = [ '#21fffb', '#ff9900', '#c0ff21']
    
    df_defects = df1.dropna(subset = defects)
    df_shifts1 = df_defects[df_defects["Shift"]==1].count()[0]
    df_shifts2 = df_defects[df_defects["Shift"]==2].count()[0]
    df_shifts3 = df_defects[df_defects["Shift"]==3].count()[0]
    labels = ["FirstShift", "SecondShift", "ThirdShift"]
    
    values = [df_shifts1, df_shifts2, df_shifts3]
    fig = go.Figure([go.Pie(labels = labels, values = values)])
    fig.update_traces(hoverinfo = "label+percent", textinfo = "value", textfont_size = 20, 
                       marker = dict(colors = colors, line = dict(color = '#222222', width = 1)))
    fig.update_layout(title_text="On What Shift", template= "plotly_dark")
    return fig


