
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from nav import navigation
import dash
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import textwrap

dash.register_page(__name__,path='/viewscore',title="View Score")

layout = html.Div(children=[
    navigation.navbar,
])
