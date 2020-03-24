import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go



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

layout= [
    html.Div(
        html.Div(
    children =[
    html.Div(html.H1("Underconstruction"),
    style= {"color":"white", 'margin': 'auto'}),
    html.Div(
    html.Img(src=app.get_asset_url("building.png")),
    style={'margin':"auto" }
    ),
    ],),style={'margin':"auto" ,'width':"500px"},),
    ]

     
