import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from panels import parts, defects, machine, current
import numpy as np
import pandas as pd
from dash.dependencies import State, Input, Output
#from dash.exceptions import PreventUpdate

import datetime
from datetime import datetime as dt
import os
import time
from app import app


# app = dash.Dash(
#     __name__,
#     meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
# )
# app.config.suppress_callback_exceptions = True
# server = app.server

app.layout = html.Div(
    [
         html.Div(
            className="row header",
            children=[
                html.Button(id="menu", children=dcc.Markdown("&#8801")),
                html.Span(
                    className="app-title",
                    children=[
                        dcc.Markdown("**CSP-Huntington**"),
                        html.Span(
                            id="subtitle",
                            children=dcc.Markdown("&nbsp using Huntington Data Only"),
                            style={"font-size": "1.8rem", "margin-top": "15px"},
                        ),
                    ],
                ),
                html.Img(src=app.get_asset_url("logo.png")),
                html.A(
                    id="learn_more",
                    children=html.Button("Learn More"),
                    className = 'button3',
                    href="https://www.cspplastics.com/",
                ),
            ],
        ),
        html.Div(
            id="tabs",
            className="row tabs",
            children=[
                dcc.Link("By Parts", href="/parts",className = 'tab1'),
                dcc.Link("By Defect Types", href="/defects", className ='tab2'),
                dcc.Link("Machine Learning Analysis", href="/machine", className = 'tab3'),
                dcc.Link("Current Situations", href ='/current', className = 'tab4'),
            ],
        ),
        # html.Div(
        #     id="mobile_tabs",
        #     className="row tabs",
        #     style={"display": "none"},
        #     children=[
        #         dcc.Link("By Parts", href="/"),
        #         dcc.Link("By Defect Types", href="/"),
        #         dcc.Link("Machine Learning Analysis", href="/"),
        #     ],
        # ),
        dcc.Location(id="url", refresh=False),
        html.Div(id="tab_content"),
    #     html.Div([
    #     # represents the URL bar, doesn't render anything
    #         dcc.Location(id='url', refresh=False),

    #         dcc.Link( href='/'),
         
    #         dcc.Link( href='/defects'),
    #         dcc.Link( href='/machine'),

    # #content will be rendered in this element
    # html.Div(id='page-content')
    # ],
    # className = "row",
    # style = {"margin":'0%'},
    #     ),
    ],)


@app.callback(
    [
        Output("tab_content", "children"),
        # Output("tabs", "children"),
        # Output("mobile_tabs", "children"),
    ],
    [Input("url", "pathname")],
)
def display_page(pathname):
    tabs = [
        dcc.Link("By Parts", href="/DefectsAnalysis/parts"),
        dcc.Link("By Defect Types", href="/DefectsAnalysis/defects"),
        dcc.Link("Machine Learning Analysis", href="/DefectsAnalysis/machine"),
        dcc.Link("Current Situations", href = '/DefectsAnalysis/current'),
    ]
    if pathname == "/defects":
        tabs[1] = dcc.Link(
            dcc.Markdown("**&#9632 By Defect Types**"),
            href="/DefectsAnalysis/defects",
        )
        return defects.layout
    elif pathname == "/machine":
        tabs[2] = dcc.Link(
            dcc.Markdown("**&#9632 Machine Learning Analysis**"), href="/DefectsAnalysis/machine"
        )
        return machine.layout
    elif pathname == "/current":
        tabs[3] = dcc.Link(
            dcc.Markdown("**&#9632 Current Situations**"), href="/DefectsAnalysis/current"
        )
        return current.layout
    else:
        tabs[0] = dcc.Link(
            dcc.Markdown("""**[&#9632 By Parts]**"""), href="/parts"
    )
    return parts.layout

        
















if __name__ == "__main__":
    app.run_server(debug=True, port =8051)