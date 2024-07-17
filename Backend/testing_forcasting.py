import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask,jsonify,request,json
import dash_bootstrap_components as dbc
from flask_cors import CORS  # Import the CORS module

import pandas as pd
from datetime import datetime as dt
from datetime import date, time
from datetime import timedelta
import calendar
import os
import pathlib
import numpy as np
# import numpy_financial as npf
from scipy.integrate import trapz
import math

import plotly
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

filename_forecast = "Administration Building.xlsx"
data_forecast_filepath = os.path.join(directory, data_folder, filename_forecast)
file_forecast = pd.ExcelFile(data_forecast_filepath)
df_forecast = file_forecast.parse("PyLoad")





#Get date and time and combine into datetime variable
startDateLP = date(2019,1,1)
startTimeLP = time(00,00)
endDateLP = date(2019,1,1)
endTimeLP = time(23,59)
startDateTimeLP = dt.combine(startDateLP, startTimeLP)
endDateTimeLP = dt.combine(endDateLP, endTimeLP)
#filter the dateframe by the date range and set x and y variables
filtered_df_forecast = df_forecast[(df_forecast['Date'].dt.date >= startDateLP) & (df_forecast['Date'].dt.date <= endDateLP)]
xDateTime = filtered_df_forecast.loc[:,"Date"].values.astype('datetime64[m]') 
length = len(xDateTime)
monthlyDemandData = filtered_df_forecast.loc[:,"Demand"].values
#create date plot and formatting
fig_LPbyDate = make_subplots(rows=1, cols=1)    
fig_LPbyDate.update_xaxes(tickformat="%m/%d \n%H:%M", title_text="Date")
fig_LPbyDate.update_layout(
    xaxis=dict(tickangle=-45),
    title= "Forecasted Load Profile: " + buildingName + " \nDate Range: " + startDateTimeLP.strftime("%m/%d/%y %H:%M") + " - " + endDateTimeLP.strftime("%m/%d/%y %H:%M"),
    xaxis_title="Date",
    yaxis_title="Demand (kW)",
    legend=dict(orientation="h"),
    margin=dict(l=10, r=10, t=30, b=20),
    showlegend=False
)
fig_LPbyDate.add_trace(
    go.Scatter(x=xDateTime, y=monthlyDemandData, mode="lines")
)
avg_forecast_demand = filtered_df_forecast["Demand"].mean() 
array_avg_forecast_demand = np.full(length, avg_forecast_demand)
fig_LPbyDate.add_trace(
    go.Scatter(x=xDateTime, y=array_avg_forecast_demand, mode="lines", name="Average Forecasted Demand",
               line=dict(color="green", dash="dash"))
)
# Peak Monthly Demand (red dashed)
peak_forecast_demand = filtered_df_forecast["Demand"].max() 
array_peak_forecast_demand = np.full(length, peak_forecast_demand)
fig_LPbyDate.add_trace(
    go.Scatter(x=xDateTime, y=array_peak_forecast_demand, mode="lines", name="Peak Forecasted Demand",
               line=dict(color="red", dash="dash"))
)
fig_LPbyDate.update_layout(showlegend=True)