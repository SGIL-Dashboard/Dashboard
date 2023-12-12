#import all the modules
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask
import dash_bootstrap_components as dbc


import pandas as pd
import datetime as dt
import os
import numpy as np


import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#initiate the app
server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

#file list

'''
paths to load profiles for each building (copy/paste in filepath)
---------------------------------------------------------------
"c:/Users/SGIL/ESS/AdminPyLoad.xlsx"
"c:/Users/SGIL/ESS/BaskervillePyLoad.xlsx"
"c:/Users/SGIL/ESS/Compton-GoethalsPyLoad.xlsx"
"c:/Users/SGIL/ESS/HarrisPyLoad.xlsx"
"c:/Users/SGIL/ESS/MarshakPyLoad.xlsx"
"c:/Users/SGIL/ESS/NAC_BoilerPyLoad.xlsx"
"c:/Users/SGIL/ESS/NAC_NorthsidePyLoad.xlsx"
"c:/Users/SGIL/ESS/ShepardPyLoad.xlsx"
"c:/Users/SGIL/ESS/SteinmannPyLoad.xlsx"
"c:/Users/SGIL/ESS/WingatePyLoad.xlsx"
'''

# gets the excel file from list above, and parses the data on the PyLoad sheet
filepath = "c:/Users/SGIL/ESS/AdminPyLoad.xlsx"
file = pd.ExcelFile(filepath)
df=file.parse("PyLoad")
buildingName = os.path.basename(filepath).replace('PyLoad.xlsx','')
'''
#split out the Date column into discreet date and time columns 
df["Day"] = df["Date"].dt.day
df["DayofWeek"] = df["Date"].dt.day_of_week
df["Month"] = df["Date"].dt.month
df["MonthDay"] = df["Date"].dt.date
df["Year"] = df["Date"].dt.year
df["Hour"] = df["Date"].dt.hour
df["Minute"] = df["Date"].dt.minute
#df.to_excel('c:/Users/SGIL/IndStudy/df.xlsx', index=False)
'''
df.set_index('Date', inplace=True)

# Resample the data to hourly demand
hourly_demand = df.resample('H').mean()

# Create new columns for date and hour
hourly_demand['Hour'] = hourly_demand.index.hour
hourly_demand['Month'] = hourly_demand.index.month


# Create a DataFrame with all hours and months
all_hours = pd.DataFrame({'Hour': np.tile(np.arange(24), len(np.unique(df.index.month))),
                          'Month': np.repeat(np.unique(df.index.month), 24)})

# Merge the demand data with the DataFrame containing all hours and months
merged_demand = pd.merge(all_hours, hourly_demand, on=['Hour', 'Month'], how='left')


# Pivot the data to get it in the desired format
pivoted_demand = hourly_demand.pivot_table(values='Demand', index='Hour', columns='Month')
#pivoted_demand.to_excel('c:/Users/SGIL/IndStudy/pivoted_demand.xlsx', index=False)
#pivoted_demand.to_excel('c:/Users/SGIL/IndStudy/pivoted_demand_merged.xlsx', index=False)

# Convert to arrays for plotting
x = np.array(pivoted_demand.index)
y = np.array(pivoted_demand.columns)
z = np.array(pivoted_demand)
fig_month_title = 'Load Profile for ' + buildingName + ': Monthly Variation' 

fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
fig.update_layout(title=fig_month_title, autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

fig.update_layout(scene=dict(
    xaxis_title='Hour',
    yaxis_title='Month',
    zaxis_title='Demand'
))

# Increase the ncontours parameter to potentially display more data points
#fig.update_traces(contours=50)  # Adjust this value as needed

#build the components
Header_component = html.H1("Ranking BESS for Urban Building Portfolios", style = {'color':'darkcyan'})

#components: visual

'''
#component: 3D daily variation
def create_surface_plot():
    fig_days = plt.figure()
    fig_days_title = 'Load Profile for ' + buildingName + ': Daily Variation'
    ax = fig_days.add_subplot(111, projection='3d')
    ax.plot_trisurf(df["DayofWeek"], df["Hour"], df['Demand'], cmap='inferno')
    ax.set_xlabel('Day: Monday (0) to Sunday (6)')
    ax.set_ylabel('Hour')
    ax.set_zlabel('Demand (kW)')
    ax.set_title(fig_days_title)
    return fig_days
#plt.show()

fig_month = plt.figure()
fig_month_title = 'Load Profile for ' + buildingName + ': Monthly Variation' 
ax = fig_month.add_subplot(111, projection='3d')
ax.plot_trisurf(df["Month"], df["Hour"], df['Demand'], cmap='inferno')
ax.set_xlabel('Month')
ax.set_ylabel('Hour')
ax.set_zlabel('Demand (kW)')
ax.set_title(fig_month_title)
#plt.show()


comp_3D_daily_x = df["DayofWeek"]
comp_3D_daily_y = df["Hour"]
comp_3D_daily_z = df['Demand']
comp_3D_daily_title = 'Load Profile for ' + buildingName + ': Daily Variation'
#comp_3D_daily_plot = go.FigureWidget()
comp_3D_daily_plot = go.FigureWidget(data=[go.Surface(z=comp_3D_daily_z, x=comp_3D_daily_x, y=comp_3D_daily_y)])
#comp_3D_daily_plot.add_surface(data=[go.Surface(z=comp_3D_daily_z, x=comp_3D_daily_x, y=comp_3D_daily_y)])

comp_3D_daily_plot.update_layout(title=comp_3D_daily_title, autosize=False,width=500, height=500, margin=dict(l=65, r=50, b=65, t=90))
#, autosize=False,width=500, height=500, margin=dict(l=65, r=50, b=65, t=90)

#component: 3D monthly variation
comp_3D_monthly_x = df["Month"]
comp_3D_monthly_y = df["Hour"]
comp_3D_monthly_z = df['Demand']
comp_3D_monthly_title = 'Load Profile for ' + buildingName + ': Monthly Variation'
comp_3D_monthly_plot = go.FigureWidget()
comp_3D_monthly_plot.add_surface(z=comp_3D_monthly_z, x=comp_3D_monthly_x, y=comp_3D_monthly_y)

#data=[go.Surface(z=comp_3D_monthly_z, x=comp_3D_monthly_x, y=comp_3D_monthly_y)]
comp_3D_monthly_plot.update_layout(title=comp_3D_monthly_title)
#, autosize=False,width=500, height=500, margin=dict(l=65, r=50, b=65, t=90)
'''
#component: max daily avg load vs peak demand


#component: monthly load profile vs peak demand


#component: data points



#design the layout
app.layout = html.Div(
    [
        dbc.Row([
            Header_component,
            dcc.Graph(figure= fig)
        ]),
        dbc.Row([
           # dbc.Col([dcc.Graph(figure= comp_3D_daily_plot)]),
           # dbc.Col([dcc.Graph(figure= comp_3D_monthly_plot)])
        ]),

        dbc.Row([
            dbc.Col(),
            dbc.Col(),
            dbc.Col()
        ]),

    ]
)
'''
# Callback to update the 3D surface plot
@app.callback(
    Output('surface-plot', 'figure'),
    Input('surface-plot', 'relayoutData')
)

def update_surface_plot(relayoutData):
    return create_surface_plot()

def update_surface_plot(relayoutData):
    fig_days = go.Figure(data=[go.Surface(
        x=df["DayofWeek"],
        y=df["Hour"],
        z=df['Demand'],
        colorscale='inferno'
    )])
    fig_days.update_layout(scene=dict(
        xaxis_title='Day: Monday (0) to Sunday (6)',
        yaxis_title='Hour',
        zaxis_title='Demand (kW)'
    ), title="Load Profile: Daily Variation")

    return fig_days

'''

#run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    