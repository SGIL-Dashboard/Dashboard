#import all the modules
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask
import dash_bootstrap_components as dbc


import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import calendar
import os
import pathlib
import numpy as np
from scipy.integrate import trapz
import math


import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#initiate the app
server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

#file list

'''
paths to load profiles for each building (copy/paste in filepath)
---------------------------------------------------------------
"AdminPyLoad.xlsx"
"BaskervillePyLoad.xlsx"
"Compton-GoethalsPyLoad.xlsx"
"HarrisPyLoad.xlsx"
"MarshakPyLoad.xlsx"
"NAC_BoilerPyLoad.xlsx"
"NAC_NorthsidePyLoad.xlsx"
"ShepardPyLoad.xlsx"
"SteinmannPyLoad.xlsx"
"WingatePyLoad.xlsx"
'''
#-------------------- Start Get Data  -----------------------------------------------------

# gets the excel file from list above, and parses the data on the PyLoad sheet

filename = "AdminPyLoad.xlsx"
data_folder = "data"
results_folder = "results"
directory = pathlib.Path(__file__).parent.resolve()
data_filepath = os.path.join(directory, data_folder, filename)
file = pd.ExcelFile(data_filepath)
df=file.parse("PyLoad")
buildingName = filename.replace('PyLoad.xlsx','')

#-------------------- End Get Data --------------------------------------------------------

#-------------------- Start Create General DF ---------------------------------------------------------------

#split out the Date column into discreet date and time columns
df["Idx"] = df["Date"]
df["Day"] = df["Date"].dt.day
df["DayofWeek"] = df["Date"].dt.dayofweek
df["Month"] = df["Date"].dt.month
df["MonthDay"] = df["Date"].dt.day
df["Year"] = df["Date"].dt.year
df["Hour"] = df["Date"].dt.hour
df["Minute"] = df["Date"].dt.minute
df.set_index('Idx', inplace=True)
results_filepath = os.path.join(directory, results_folder)
df.to_excel(os.path.join(directory, results_folder, "df_index_code.xlsx"), index=False)

#-------------------- End General Create DFs ---------------------------------------------------------------

#---------------------Start Create Monthly Data DF (bar chart) ----------------------------------------------------------

#aggregate data
maxMonthlyValue = df.groupby(["Year","Month"])["Demand"].aggregate(peakMonthlyDemand = 'max') 
avgMonthlyValue = df.groupby(["Year", "Month"])["Demand"].aggregate(avgMonthlyDemand = 'mean')
peakDemand = df["Demand"].max() 
avgDailyValue = df.groupby(["Year", "Month","Day"])["Demand"].aggregate(dailyAvgDemand = 'mean')
maxAvgValue = avgDailyValue.groupby(["Year","Month"])["dailyAvgDemand"].aggregate(maxAvgDemand = 'max')

avgMonthlyDemand = avgMonthlyValue.values.flatten()
peakMonthlyDemand = maxMonthlyValue.values.flatten()
peakDailyDemand = maxAvgValue.values.flatten()
maxPeakDailyDemand = peakDailyDemand.max()
monthlyPeakDemandShaving = peakMonthlyDemand - peakDailyDemand
maxPeakDemandShaving = monthlyPeakDemandShaving.max()

monthly_data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "MonthlyPeakDemand": peakMonthlyDemand,
    "MaxDemandShaving": monthlyPeakDemandShaving,
    "PeakDailyDemand": peakDailyDemand,
 }
aggregated_df = pd.DataFrame(monthly_data)

aggregated_df.to_excel(os.path.join(directory, results_folder, "aggregated_df.xlsx"), index=False)

#'''---------------------- End Create Monthly Data DF ---------------------------------------------------------


#'''---------------------- Start Create BESS DF -------------------------------------------------------

#create a dataframe to store ESS charging and discharging data
dispatchSchedule = pd.DataFrame(columns=['Month','Energy','Duration','StartTime','EndTime','Charge','SOC'])
currentMonth = []
currentPeak = 0

#loop through file to get data by month
maxstateofCharge = 1
maxESS = 0
minSOC = -1
dod = .15

while (minSOC < 1 or 1-dod < maxESS/maxstateofCharge):
    #print("minSOC: ", minSOC)
    #print("maxstateofCharge: ", maxstateofCharge)
    
    for i in range(1,13):
        monthName = calendar.month_name[i]
        #print(monthName)

        #Get data for the month
        currentMonthDataDF = df.loc[df["Date"].dt.month == i]
        currentPeakDemand = peakDailyDemand[i-1]
        xDateTime = currentMonthDataDF.loc[:,"Date"].values.astype('datetime64[m]') 
        yDemandData = currentMonthDataDF.loc[:,"Demand"].values
        
        #find the indices where the two currentPeakDemand curve intersects the DemandData curve
        idx = np.argwhere(np.diff(np.sign(currentPeakDemand - yDemandData))).flatten()
        sizeofidx = xDateTime[idx].shape

        #maxStateofCharge is the highest charge the battery can attain, stateOfCharge is the current SOC of the battery
        #set to 0 initially, then set to ESS capacity to determine the battery size. 
        #Make sure min SOC does not fall below the required depth of discharge
        maxstateofCharge = maxstateofCharge
        stateOfCharge = maxstateofCharge
        #print("stateOfCharge: ", stateOfCharge)
        
        #loop through indicies to calculate the energy charging and discharging by integrating 
        # between the start and end times (where the 2 curves cross)
        for j in range(0,sizeofidx[0] -1):
            
            #determine the start and end times to integrate
            startDate = xDateTime[idx][j]
            endDate = xDateTime[idx][j+1]

            #create a boolean mask for the datetime range indicated: (e.g. [False, False, True, True, False, False]) 
            mask = (currentMonthDataDF["Date"] > startDate) & (currentMonthDataDF["Date"] <= endDate)
            
            #create demand arrays with the data from the time range that was masked
            demandIntegrate  = currentMonthDataDF.loc[:,"Demand"][mask].values  
            
            #create date arrays with data from the time range that was masked. convert data from datetime64[ns]
            #to datetime64[m]. Then take the size of that new array and convert it to a an array of the same 
            #size with integer elements starting at zero and going to size-1
            dateIntegrate_ns = currentMonthDataDF.loc[:,"Date"][mask].values
            dateIntegrate_m = dateIntegrate_ns.astype('datetime64[m]')
            dateIntegrate_int = np.arange(dateIntegrate_m.shape[0])
        
            #integrate over the demand (kW) curve between the start and end times indicated with the x intervals = 1 for
            #each 15 min interval. Therefore, to get kWh, divide the energy result by 4 
            energy_under_curve = trapz(demandIntegrate, dateIntegrate_int)
            energy_under_line = trapz(currentPeakDemand * np.ones_like(demandIntegrate), dateIntegrate_int)
            energy = (energy_under_curve - energy_under_line).astype(timedelta)/4
            duration = (dateIntegrate_int.shape[0]-1)*15
            charge = math.copysign(1,energy)
        
            #does not allow the state of charge to go above the possible maxstateofCharge
            if maxstateofCharge > 0 and  maxstateofCharge < energy*-1 + stateOfCharge:
                stateOfCharge = maxstateofCharge
            else:
                stateOfCharge = energy * -1 + stateOfCharge
            
            essData = {'Month': monthName,'Energy': energy,'Duration': duration,'StartTime': startDate,'EndTime': endDate,'Charge': charge,'SOC': stateOfCharge} 
            dispatchSchedule.loc[len(dispatchSchedule)] = essData
    
    minSOC = dispatchSchedule['SOC'].min()
    maxESS = dispatchSchedule['Energy'].max()
    maxstateofCharge = math.ceil(maxESS / (1-dod))
    #print("dispatchSchedule: ", dispatchSchedule)
    essData = {}
    ESSCapacity = dispatchSchedule
    dispatchSchedule = pd.DataFrame(columns=['Month','Energy','Duration','StartTime','EndTime','Charge','SOC'])

#cost variables (can possibly be set with filters)
OMCost_kWh = 24.25
OMCost_fixed = 0
capitalCost_kWh = 967.50
capitalCost_kW = 0
footprint_kWh = 37 #in cm^2 using values from Tesla Megapack  

#BESS variables
BESS_capacity = maxstateofCharge
power_duration = 4 # Use duration to calculate power based on BESS Capacity. N/A (0) uses maxpower needed to shave the peak
if power_duration == 0:
    BESS_power = math.ceil(maxPeakDemandShaving)
if power_duration > 0:
    BESS_power = math.ceil(maxstateofCharge/power_duration)    
BESS_cost = (OMCost_kWh * BESS_capacity + OMCost_fixed) + (capitalCost_kWh * BESS_capacity + capitalCost_kW * BESS_power)
BESS_footprint = BESS_capacity * footprint_kWh

#print statements
print("Building: ", buildingName)
print('BESS Capacity (kWh): ', BESS_capacity)
print('BESS Power (kW): ', BESS_power)
print("BESS Cost ($): ", BESS_cost)
print("BESS Footprint (cm^2): ", BESS_footprint)

#-------------------------End Create BESS DF -----------------------------------------------------------'''

#'''-------------------- Start Create Pivots for 3D Graphs -----------------------------------------------

# Resample the data to average hourly demand
monthly_resample = df.resample('H').mean()
daily_resample = df.resample('H').mean()

# Create new columns for month and hour
monthly_resample['Hour'] = monthly_resample.index.hour
monthly_resample['Month'] = monthly_resample.index.month

daily_resample['Hour'] = monthly_resample.index.hour
daily_resample['DayofWeek'] = monthly_resample.index.dayofweek


# Pivot the data to get it in the desired format
monthly_pivot = monthly_resample.pivot_table(values='Demand', index='Hour', columns='Month')
daily_pivot = daily_resample.pivot_table(values='Demand', index='Hour', columns='DayofWeek')

monthly_pivot.to_excel(os.path.join(directory, results_filepath, 'monthly_pivot.xlsx'), index=False)
daily_pivot.to_excel(os.path.join(directory, results_filepath, 'daily_pivot.xlsx'), index=False)

#-------------------- End Create Pivots for 3D Graphs -----------------------------------------------'''


#--------------------- Start Build the components ---------------------------------------------------------

Header_component = html.H1("Ranking BESS for Urban Building Portfolios", style = {'color':'darkcyan'})


#-----------------------component: comp_3D_daily_plot----------------------------

x_daily = np.array(daily_pivot.index)
y_daily = np.array(daily_pivot.columns)
z_daily = np.array(daily_pivot)
fig_daily_title = 'Load Profile for ' + buildingName + ': Daily Variation' 

comp_3D_daily_plot = go.Figure(data=[go.Surface(z=z_daily, x=x_daily, y=y_daily)])
comp_3D_daily_plot.update_layout(title=fig_daily_title, autosize=True)

comp_3D_daily_plot.update_layout(scene=dict(
    xaxis_title='Hour',
    yaxis_title='Day of Week',
    zaxis_title='Demand'
))

#----------------------component: comp_3D_monthly_plot----------------------------

x_monthly = np.array(monthly_pivot.index)
y_monthly = np.array(monthly_pivot.columns)
z_monthly = np.array(monthly_pivot)
fig_month_title = 'Load Profile for ' + buildingName + ': Monthly Variation' 

comp_3D_monthly_plot = go.Figure(data=[go.Surface(z=z_monthly, x=x_monthly, y=y_monthly)])
comp_3D_monthly_plot.update_layout(title=fig_month_title, autosize=False)

comp_3D_monthly_plot.update_layout(scene=dict(
    xaxis_title='Hour',
    yaxis_title='Month',
    zaxis_title='Demand'
))

#---------------component: max daily avg load vs peak demand---------------------------------------

peak_demand_bar = px.bar(aggregated_df, x="Month", y=["PeakDailyDemand", "MaxDemandShaving"],
             title="Monthly Peak and Average Demand: " + buildingName,
             labels={"value": "Demand"},
             hover_name="Month", 
             hover_data=["MonthlyPeakDemand"],
             height=400)

peak_demand_bar.update_layout(
    legend=dict(orientation="h"),
    margin=dict(l=10, r=10, t=15, b=10)
    )             

#------------------component: monthly load profile ---------------------------

#Get data for the chosen month
monthValue = 1
monthName = calendar.month_name[monthValue]
currentMonthDataDF = df.loc[df["Date"].dt.month == monthValue]
xDateTime = currentMonthDataDF.loc[:,"Date"].values.astype('datetime64[m]') 

# Create a subplot with one plot for all curves
fig_monthlyDemand = make_subplots(rows=1, cols=1)    

# Update x-axis date formatting
fig_monthlyDemand.update_xaxes(tickformat="%m/%d", title_text="Date")

# Update layout
fig_monthlyDemand.update_layout(
    xaxis=dict(tickangle=-45),
    title= monthName + " Load Profile: " + buildingName,
    xaxis_title="Date",
    yaxis_title="Demand (kW)",
    legend=dict(orientation="h"),
    margin=dict(l=10, r=10, t=15, b=10),
    showlegend=True
)

# 15 Minute Demand Data Plot
monthlyDemandData = currentMonthDataDF.loc[:,"Demand"].values
fig_monthlyDemand.add_trace(
    go.Scatter(x=xDateTime, y=monthlyDemandData, mode="lines", name="15 Minute Demand Data")
)

# Peak Daily Avg Demand (yellow dashed)
peakDailyAvgDemandData = peakDailyDemand[monthValue-1]
fig_monthlyDemand.add_trace(
    go.Scatter(x=[min(xDateTime), max(xDateTime)],
               y=[peakDailyAvgDemandData, peakDailyAvgDemandData],
               mode="lines",
               name="Peak Daily Avg. Demand",
               line=dict(color="yellow", dash="dash"))
)

# Monthly Avg Demand (green dashed)
avgMonthlyDemandData = avgMonthlyDemand[monthValue-1]
fig_monthlyDemand.add_trace(
    go.Scatter(x=[min(xDateTime), max(xDateTime)],
               y=[avgMonthlyDemandData, avgMonthlyDemandData],
               mode="lines",
               name="Monthly Avg. Demand",
               line=dict(color="green", dash="dash"))
)

# Peak Monthly Demand (red dashed)
peakMonthlyDemandData = peakMonthlyDemand[monthValue-1]
fig_monthlyDemand.add_trace(
    go.Scatter(x=[min(xDateTime), max(xDateTime)],
               y=[peakMonthlyDemandData, peakMonthlyDemandData],
               mode="lines",
               name="Peak Demand",
               line=dict(color="red", dash="dash"))
)


#------------------------------------------End Build the Components ------------------------------------------'''

#'''------------------------------------ Start Create the Layout ----------------------------------------------
#design the layout
app.layout = html.Div(children=[ #1
    
    html.Div(children=[ #1.1
        html.H3(children='Analyzing Load Profile Data for Urban Buildings'),
        html.H4(children='Determining BESS Suitability', style={'marginTop': '-10px', 'marginBottom': '25px'})
    ], style={'textAlign': 'center', 'color':'#e3e3e3'}),
   
    html.Div(children=[ #1.2
        html.Div(children=[ #1.2.1
            
            
            
            html.Label('Filter by date (M-D-Y):'),
            dcc.DatePickerRange(
                id='input_date',
                month_format='DD/MM/YYYY',
                show_outside_days=True,
                minimum_nights=0,
                initial_visible_month=dt(2019, 1, 1),
                min_date_allowed=dt(2019, 1, 1),
                max_date_allowed=dt(2019, 12, 31),
                start_date=dt.strptime("2018-06-01", "%Y-%m-%d").date(),
                end_date=dt.strptime("2018-12-31", "%Y-%m-%d").date()
            ),

            html.Label('Month to Analyze:', style={'paddingTop': '2rem'}),
            dcc.Dropdown(
                id='input_days',
                options=[
                    {'label': 'January', 'value': '1'},
                    {'label': 'February', 'value': '2'},
                    {'label': 'March', 'value': '3'},
                    {'label': 'April', 'value': '4'},
                    {'label': 'May', 'value': '5'},
                    {'label': 'June', 'value': '6'},
                    {'label': 'July', 'value': '7'},
                    {'label': 'August', 'value': '8'},
                    {'label': 'September', 'value': '9'},
                    {'label': 'October', 'value': '10'},
                    {'label': 'November', 'value': '11'},
                    {'label': 'December', 'value': '12'}
                ],
                value=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','12'],
                multi=False
            ),

            html.Label('Load Profile Curves:', style={'paddingTop': '1rem', 'display': 'inline-block'}),
            dcc.Checklist(
                id='input_acc_sev',
                options=[
                    {'label': '   Peak Daily Avg. Demand', 'value': '1'},
                    {'label': '   Monthly Avg. Demand', 'value': '2'},
                    {'label': '   Peak Demand', 'value': '3'}
                ],
                value=['1', '2', '3'],
            ),

            html.Label('BESS Depth of Discharge (%):', style={'paddingTop': '2rem'}),
            dcc.RangeSlider(
                    id='input_dod',
                    min=0,
                    max=100,
                    step=1,
                    value=[0, 100],
                    marks={
                        0: '0',
                        20: '20',
                        40: '40',
                        60: '60',
                        80: '80',
                        100: '100'
                    },
            ),

            html.Label('BESS Footprint (cm^2/ kWh):', style={'paddingTop': '2rem'}),
            dcc.RangeSlider(
                    id='input_footprint',
                    min=10,
                    max=100,
                    step=1,
                    value=[10, 100],
                    marks={
                        10: '10',
                        20: '20',
                        30: '30',
                        40: '40',
                        50: '50',
                        60: '60',
                        70: '70',
                        80: '80',
                        90: '90',
                        100: '100'
                    },
            ),

            html.Label('Battery Duration', style={'paddingTop': '2rem'}),
            dcc.Dropdown(
                id='input_duration',
                options=[
                    {'label': '4 hours', 'value': 4},
                    {'label': '3 hours', 'value': 3},
                    {'label': '2 hours', 'value': 2},
                    {'label': '1 hour', 'value': 1},
                    {'label': 'N/A', 'value': 0}
                ],
                value=[1, 2, 3, 4, 0],
                multi=False
            ),

            html.Label('BESS Capital Costs ($/kWh):', style={'paddingTop': '2rem'}),
            dcc.Input(
            id="input {}".format("number"),
            type="number",
            placeholder="225.00".format("number")
            ),
            html.Label('BESS Capital Costs ($/kW):', style={'paddingTop': '2rem'}),
            dcc.Input(
            id="input {}".format("number"),
            type="number",
            placeholder="405.00".format("number")
            ),
            html.Label('BESS O&M Costs ($/kWh):', style={'paddingTop': '2rem'}),
            dcc.Input(
            id="input {}".format("number"),
            type="number",
            placeholder="10.00".format("number")
            ),
            html.Label('BESS O&M  Costs ($/year):', style={'paddingTop': '2rem'}),
            dcc.Input(
            id="input {}".format("number"),
            type="number",
            placeholder="40000.00".format("number")
            ),

        ], className="col-md-3", 
        style={'padding':'.5rem', 'margin':'.5rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem', 'backgroundColor': 'white'}),
        
        html.Div(children=[ #1.2.2
            html.Div(children=[ #1.2.2.1
                html.Div(children=[
                    html.H3(id='no_acc', style={'fontWeight': 'bold'}),
                    html.Label('BESS Capacity'),
                ], className="col-md-2 number-stat-box",
                style={'padding':'.5rem', 'margin':'.5rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white',}
                ), 

                html.Div(children=[ 
                    html.H3(id='no_cas', style={'fontWeight': 'bold', 'color': '#f73600'}),
                    html.Label('BESS Power'),
                ], className="col-md-2 number-stat-box",
                style={'padding':'.5rem', 'margin':'.5rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white',}
                ), 

                html.Div(children=[ 
                    html.H3(id='no_veh', style={'fontWeight': 'bold', 'color': '#00aeef'}),
                    html.Label('BESS Cost'),
                ], className="col-md-2 number-stat-box",
                style={'padding':'.5rem', 'margin':'.5rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white',}
                ), 

                html.Div(children=[ 
                    html.H3(id='no_days', style={'fontWeight': 'bold', 'color': '#a0aec0'}),
                    html.Label('BESS Footprint'),
                ], className="col-md-2 number-stat-box",
                style={'padding':'.5rem', 'margin':'.5rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white',}
                ), 
            ], style={'margin':'.1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'flex-wrap': 'wrap'}),

            html.Div(children=[ #1.2.2.2
                html.Div(children=[ #1.2.2.2
                    dcc.Graph(figure= fig_monthlyDemand)
                ], className="col-md-7 number-stat-box",
                style={'padding':'.3rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white',}
                ), 

                html.Div(children=[ #1.2.2.2
                    dcc.Graph(figure= peak_demand_bar)
                ],className="col-md-4 number-stat-box",
                style={'padding':'.3rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white',}
                ), 
            ], className="col-md-12", 
            style={'margin':'1rem', 'marginBottom':'2rem','display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'flex-wrap': 'wrap'}),
        
        ], #close div 1.2.2
        className="col-md-8"),
          
          html.Div(children=[ #1.3
            dbc.Row([
            dbc.Col([dcc.Graph(figure= comp_3D_daily_plot)], width=5),
            dbc.Col([dcc.Graph(figure= comp_3D_monthly_plot)], width=5),
            dbc.Col()
            ])
        ])

    ], className="row", style={'margin':'2rem', 'padding': '1rem', 'display': 'flex', 'backgroundColor': '#f2f2f2', 'justify-content': 'center'}), 

html.Div(children=[ #1.1
        html.H3(children='Analyzing Load Profile Data for Urban Buildings'),
        html.H4(children='Determining BESS Suitability', style={'marginTop': '-10px', 'marginBottom': '25px'})
    ], style={'textAlign': 'center', 'color':'#e3e3e3'}),

], style={'backgroundColor': '#47637D', 'margin': '2rem'})


#---------------------------------- End Create the Layout ----------------------------------------------
#run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    