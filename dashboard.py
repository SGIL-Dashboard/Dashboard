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
"c:/Users/SGIL/IndStudy/data/AdminPyLoad.xlsx"
"c:/Users/SGIL/IndStudy/data/BaskervillePyLoad.xlsx"
"c:/Users/SGIL/IndStudy/data/Compton-GoethalsPyLoad.xlsx"
"c:/Users/SGIL/IndStudy/data/HarrisPyLoad.xlsx"
"c:/Users/SGIL/IndStudy/data/MarshakPyLoad.xlsx"
"c:/Users/SGIL/IndStudy/data/NAC_BoilerPyLoad.xlsx"
"c:/Users/SGIL/IndStudy/data/NAC_NorthsidePyLoad.xlsx"
"c:/Users/SGIL/IndStudy/data/ShepardPyLoad.xlsx"
"c:/Users/SGIL/IndStudy/data/SteinmannPyLoad.xlsx"
"c:/Users/SGIL/IndStudy/data/WingatePyLoad.xlsx"
'''
#-------------------- Start Get Data  -----------------------------------------------------

# gets the excel file from list above, and parses the data on the PyLoad sheet
filepath = "c:/Users/SGIL/IndStudy/data/AdminPyLoad.xlsx"
file = pd.ExcelFile(filepath)
df=file.parse("PyLoad")
buildingName = os.path.basename(filepath).replace('PyLoad.xlsx','')
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
df.to_excel('c:/Users/SGIL/IndStudy/results/df_index_code.xlsx', index=False)

#-------------------- End General Create DFs ---------------------------------------------------------------

#---------------------Start Create Monthly Data DF (bar chart) ----------------------------------------------------------

#aggregate data
maxValue = df.groupby(["Year","Month"])["Demand"].aggregate(peakDemand = 'max') 
monthlyPeakDemand = maxValue.values.flatten()
peakDemand = df["Demand"].max() 
avgValue = df.groupby(["Year", "Month","Day"])["Demand"].aggregate(dailyAvgDemand = 'mean')
maxAvgValue = avgValue.groupby(["Year","Month"])["dailyAvgDemand"].aggregate(maxAvgDemand = 'max')
peakDailyDemand = maxAvgValue.values.flatten()
maxPeakDemand = peakDailyDemand.max()
monthlyPeakDemandShaving = monthlyPeakDemand - peakDailyDemand
maxPeakDemandShaving = monthlyPeakDemandShaving.max()

monthly_data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "MonthlyPeakDemand": monthlyPeakDemand,
    "MaxDemandShaving": monthlyPeakDemandShaving,
    "PeakDailyDemand": peakDailyDemand,
 }
aggregated_df = pd.DataFrame(monthly_data)



aggregated_df.to_excel('c:/Users/SGIL/IndStudy/results/aggregated_df.xlsx', index=False)


#'''---------------------- End Create Monthly Data DF ---------------------------------------------------------


#'''---------------------- Start Create BESS DF -------------------------------------------------------


#create a dataframe to store ESS charging and discharging data
dispatchSchedule = pd.DataFrame(columns=['Month','Energy','Duration','StartTime','EndTime','Charge','SOC'])
currentMonth = []
currentPeak = 0

#loop through file to get data by month
for i in range(1,13):
    monthName = calendar.month_name[i]

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
    maxstateofCharge = 220
    stateOfCharge = maxstateofCharge
    
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
           stateOfCharge = energy*-1 + stateOfCharge
        
        essData = {'Month': monthName,'Energy': energy,'Duration': duration,'StartTime': startDate,'EndTime': endDate,'Charge': charge,'SOC': stateOfCharge} 
        dispatchSchedule.loc[len(dispatchSchedule)] = essData

maxESS = dispatchSchedule['Energy'].max()
minSOC = dispatchSchedule['SOC'].min()


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

monthly_pivot.to_excel('c:/Users/SGIL/IndStudy/results/monthly_pivot.xlsx', index=False)
daily_pivot.to_excel('c:/Users/SGIL/IndStudy/results/daily_pivot.xlsx', index=False)

#-------------------- End Create Pivots for 3D Graphs -----------------------------------------------'''


#'''--------------------- Start Build the components ---------------------------------------------------------

Header_component = html.H1("Ranking BESS for Urban Building Portfolios", style = {'color':'darkcyan'})

#components: visual


#component: comp_3D_daily_plot

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

#component: comp_3D_monthly_plot

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

#component: max daily avg load vs peak demand

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

#component: monthly load profile vs peak demand
k = 1
monthName = calendar.month_name[k]
#Get data for the month
currentMonthDataDF = df.loc[df["Date"].dt.month == k]
currentPeakDemand = peakDailyDemand[k-1]
xDateTime = currentMonthDataDF.loc[:,"Date"].values.astype('datetime64[m]') 
yDemandData = currentMonthDataDF.loc[:,"Demand"].values
    
    
#create line of length xDateTime that has values equal to the average max daily demand
size = len(xDateTime)
currentPeakDemandArray = np.empty(size, dtype=float).fill(currentPeakDemand)
    
# Create a subplot with one plot
fig_monthlyDemand = make_subplots(rows=1, cols=1)

# Add the demand data line plot
fig_monthlyDemand.add_trace(
    go.Scatter(x=xDateTime, y=yDemandData, mode="lines", name="15 Minute Demand Data")
)

# Add a trace for the peak demand line (red dashed)
fig_monthlyDemand.add_trace(
    go.Scatter(x=[min(xDateTime), max(xDateTime)],
               y=[currentPeakDemand, currentPeakDemand],
               mode="lines",
               name="Monthly Peak Demand",
               line=dict(color="red", dash="dash"))
)

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




#component: data points

'''
print("Building: ", buildingName)
print('Min SOC: ', minSOC)
print('Max Discharge: ', maxESS)
print('Update line 122 with ESS capacity.')
print('ESS capacity: ', maxESS*1.15)
print('depth of discharge: ', (maxESS*.15 ))
print("ESS power (to shave peak): ", maxPeakDemandShaving)
'''
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

            html.Label('Day of the week:', style={'paddingTop': '2rem'}),
            dcc.Dropdown(
                id='input_days',
                options=[
                    {'label': 'Sun', 'value': '1'},
                    {'label': 'Mon', 'value': '2'},
                    {'label': 'Tue', 'value': '3'},
                    {'label': 'Wed', 'value': '4'},
                    {'label': 'Thurs', 'value': '5'},
                    {'label': 'Fri', 'value': '6'},
                    {'label': 'Sat', 'value': '7'}
                ],
                value=['1', '2', '3', '4', '5', '6', '7'],
                multi=True
            ),

            html.Label('Accident Severity:', style={'paddingTop': '1rem', 'display': 'inline-block'}),
            dcc.Checklist(
                id='input_acc_sev',
                options=[
                    {'label': 'Fatal', 'value': '1'},
                    {'label': 'Serious', 'value': '2'},
                    {'label': 'Slight', 'value': '3'}
                ],
                value=['1', '2', '3'],
            ),

            html.Label('Speed limits (mph):', style={'paddingTop': '2rem'}),
            dcc.RangeSlider(
                    id='input_speed_limit',
                    min=20,
                    max=70,
                    step=10,
                    value=[20, 70],
                    marks={
                        20: '20',
                        30: '30',
                        40: '40',
                        50: '50',
                        60: '60',
                        70: '70'
                    },
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

    # Line chart for accidents per day
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


'''
app.layout = html.Div(
    [
        dcc.Input(id='username', value='Initial Value', type='text'),
        html.Button(id='submit-button', type='submit', children='Submit'),
        html.Div(id='output_div'),
        dbc.Row([
            Header_component,
            #dcc.Graph(figure= fig)
        ]),
        dbc.Row([
            dbc.Col(),
            dbc.Col([dcc.Graph(figure= peak_demand_bar)]),
            dbc.Col([dcc.Graph(figure= fig_monthlyDemand)]),
        ]),

        dbc.Row([
            dbc.Col([dcc.Graph(figure= comp_3D_daily_plot)]),
            dbc.Col([dcc.Graph(figure= comp_3D_monthly_plot)]),
            dbc.Col()
        ]),

    ]
)

@app.callback(Output('output_div', 'children'),
                  [Input('submit-button', 'n_clicks')],
                  [State('username', 'value')],
                  )
def update_output(clicks, input_value):
    if clicks is not None:
            print(clicks, input_value)
'''
#------------------------------------ End Create the Layout ----------------------------------------------'''
#run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    