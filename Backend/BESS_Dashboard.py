#import all the modules
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask,jsonify,request,json
import dash_bootstrap_components as dbc
from flask_cors import CORS  # Import the CORS module

import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import calendar
import os
import pathlib
import numpy as np
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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#initiate the app
# server = Flask(__name__)
# app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
app=Flask(__name__)
CORS(app)

#file list

'''
paths to load profiles for each building (copy/paste in filepath)
---------------------------------------------------------------
"Administration Building.xlsx"
"Baskerville Hall.xlsx"
"Compton-Goethals Hall.xlsx"
"Harris Hall.xlsx"
"Marshak Science Building.xlsx"
"NAC_Boiler.xlsx"
"NAC_Northside.xlsx"
"Shepard Hall.xlsx"
"Steinmann Hall.xlsx"
"Wingate Hall.xlsx"
'''
#-------------------- Start Get Data  -----------------------------------------------------
data_folder = "data"
results_folder = "results"
filename="Administration Building.xlsx"
directory = pathlib.Path(__file__).parent.resolve()
data_filepath = os.path.join(directory, data_folder, filename)
file = pd.ExcelFile(data_filepath)
df=file.parse("PyLoad")
buildingName = filename.replace('PyLoad.xlsx','')

maxMonthlyValue=''
avgMonthlyValue=''
peakDemand=''
avgDailyValue=''
maxAvgValue=''
avgMonthlyDemand=''
peakMonthlyDemand=''
peakDailyDemand=''
maxPeakDailyDemand=''
monthlyPeakDemandShaving=''
maxPeakDailyDemand=''
x_daily=''
peak_demand_bar=''
y_daily=''
z_daily=''
fig_daily_title=''
x_monthly=''
y_monthly=''
z_monthly=''
fig_month_title=''
peak_demand_bar=''
fig_monthlyDemand=''
MaxDemandShaving=''
bar_graph_data={}

# gets the excel file from list above, and parses the data on the PyLoad sheet
@app.route('/file_selection', methods=['POST'])
def file_selection():
    try:
        global filename,data_filepath,file,df,buildingName
        # file = request.files['file']
        # filename = request.form['filename']
        # print("we uploaded this file=",filename)
        print("we are before file processing")
        
        if 'file'  in request.files:
            print("we are in if statement")
            data=request.json
            uid=data['UID']
            
            file = request.files['file']
            filename = request.form['name'] 
             
            print("we uploaded this file=",filename)
            buildingName = filename
            df=pd.read_excel(pd.ExcelFile(file))
            print("we createed df")
            
        else:   
            print("we are in else statement") 
            # uid=request.UID
            # print("user_id is =>",uid)
            data=request.json
            uid=data['UID']
            filename=data['selectedOption']
            uid=data['UID']
            # print("data=======>",data)
            data_filepath = os.path.join(directory, data_folder, filename)
            file = pd.read_excel(data_filepath)
            df=file
            buildingName = filename.replace('.xlsx','')
        
        # df=file.parse("PyLoad")
            

        
       
        
        data_preprocessing(df,uid)
        
        return jsonify({'status':"success"})

    except:
        print("default file uid not found= >")
        return jsonify({'exception':"error"})



#-------------------- End Get Data --------------------------------------------------------

@app.route('/get_all_files', methods=['GET'])
def get_all_files():
    try:

        all_file_folder=os.path.join(directory, data_folder)
        # print(all_file_folder)
        # Get the list of files in the folder
        data_file_list = os.listdir(all_file_folder)
        # print("data_file_list=>",data_file_list)
        return jsonify({"all_file":data_file_list})
              
    except Exception as e:
        print("errror=>",e)
        return jsonify({"all_file":[]})
                

   
#-------------------- Start Create General DF ---------------------------------------------------------------
def data_preprocessing(df,uid):
    print("this function data preprocessing called")
    global maxMonthlyValue,avgMonthlyValue,peakDemand,avgDailyValue,maxAvgValue,avgMonthlyDemand
    global peakMonthlyDemand,peakDailyDemand,maxPeakDailyDemand
    global monthlyPeakDemandShaving,maxPeakDailyDemand,maxPeakDemandShaving,MaxDemandShaving
    global x_daily,y_daily,z_daily,fig_daily_title
    global x_monthly,y_monthly,z_monthly,fig_month_title
    global peak_demand_bar
    global results_folder
   




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
    results_folder=results_folder.split("/")[0]
    results_folder=results_folder+"/"+str(uid)
    # print("our result folder=>",results_folder)
    # Create the folder if it doesn't exist
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
        print("Folder created successfully")
    else:
        print("Folder already exists")

    results_filepath = os.path.join(directory, results_folder)

    # Get the list of files in the folder
    file_list = os.listdir(results_filepath)

    print(file_list)
    # Iterate through the files and delete them
    for file_name in file_list:
        file_path = os.path.join(results_filepath, file_name)
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

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
    monthlyPeakDemandShaving=np.array(monthlyPeakDemandShaving)
    print(monthlyPeakDemandShaving)
    maxPeakDemandShaving = monthlyPeakDemandShaving.max()

    monthly_data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "MonthlyPeakDemand": peakMonthlyDemand,
        "MaxDemandShaving": monthlyPeakDemandShaving,
        "PeakDailyDemand": peakDailyDemand,
    }
    
    
    bar_graph_data=monthly_data

    aggregated_df = pd.DataFrame(monthly_data)
    
    aggregated_df.to_excel(os.path.join(directory, results_folder, "aggregated_df.xlsx"), index=False)

    
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

    
    x_daily = np.array(daily_pivot.index)
    y_daily = np.array(daily_pivot.columns)
    z_daily = np.array(daily_pivot)
    fig_daily_title = 'Load Profile for ' + buildingName + ': Daily Variation' 
    x_monthly = np.array(monthly_pivot.index) 
    y_monthly = np.array(monthly_pivot.columns)
    z_monthly = np.array(monthly_pivot)
    fig_month_title = 'Load Profile for ' + buildingName + ': Monthly Variation' 

    print("WE ARE HERE","*"*50)
    # print(MaxDemandShaving,peakDailyDemand)
    print(type(peakDailyDemand),type(MaxDemandShaving))


    peak_demand_bar = px.bar( aggregated_df, x="Month", y=["PeakDailyDemand", "MaxDemandShaving"] ,
             title="Monthly Peak and Average Demand: " + buildingName,
             labels={"value": "Demand"},
             hover_name="Month", 
             hover_data=["MonthlyPeakDemand"],
             height=600,
              
            )

    peak_demand_bar.update_layout(
        legend=dict(orientation="h"),
        margin=dict(l=10, r=10, t=25, b=40)
        )  
    
    print("we are done with file creation")
    peak_demand_bar= peak_demand_bar.to_json(peak_demand_bar)

    # bar_graph_data=jsonify({"PeakDailyDemand":PeakDailyDemand,"MaxDemandShaving":MaxDemandShaving,
    #                 "buildingName":buildingName
    #                 })
  

    
    
def data_preprocessing_date(df,uid,start_date,end_date,start_time,end_time):
    print("this function data preprocessing called")
    global maxMonthlyValue,avgMonthlyValue,peakDemand,avgDailyValue,maxAvgValue,avgMonthlyDemand
    global peakMonthlyDemand,peakDailyDemand,maxPeakDailyDemand
    global monthlyPeakDemandShaving,maxPeakDailyDemand,maxPeakDemandShaving,MaxDemandShaving
    global x_daily,y_daily,z_daily,fig_daily_title
    global x_monthly,y_monthly,z_monthly,fig_month_title
    global peak_demand_bar
    global results_folder
   

    df = df[(df['date'] >= start_date) & (df['date'] <= end_date) & 
                
                   (df['start_time'] >= start_time) & (df['end_time'] <= end_time)]


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
    results_folder=results_folder.split("/")[0]
    results_folder=results_folder+"/"+str(uid)
    print("our result folder=>",results_folder)
    # Create the folder if it doesn't exist
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
        print("Folder created successfully")
    else:
        print("Folder already exists")

    results_filepath = os.path.join(directory, results_folder)

    # Get the list of files in the folder
    file_list = os.listdir(results_filepath)

    print(file_list)
    # Iterate through the files and delete them
    for file_name in file_list:
        file_path = os.path.join(results_filepath, file_name)
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

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
    monthlyPeakDemandShaving=np.array(monthlyPeakDemandShaving)
    print(monthlyPeakDemandShaving)
    maxPeakDemandShaving = monthlyPeakDemandShaving.max()

    monthly_data = {
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "MonthlyPeakDemand": peakMonthlyDemand,
        "MaxDemandShaving": monthlyPeakDemandShaving,
        "PeakDailyDemand": peakDailyDemand,
    }
    
    
    bar_graph_data=monthly_data

    aggregated_df = pd.DataFrame(monthly_data)
    
    aggregated_df.to_excel(os.path.join(directory, results_folder, "aggregated_df.xlsx"), index=False)

    
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

    
    x_daily = np.array(daily_pivot.index)
    y_daily = np.array(daily_pivot.columns)
    z_daily = np.array(daily_pivot)
    fig_daily_title = 'Load Profile for ' + buildingName + ': Daily Variation' 
    x_monthly = np.array(monthly_pivot.index)
    y_monthly = np.array(monthly_pivot.columns)
    z_monthly = np.array(monthly_pivot)
    fig_month_title = 'Load Profile for ' + buildingName + ': Monthly Variation' 

    print("WE ARE HERE","*"*50)
    # print(MaxDemandShaving,peakDailyDemand)
    print(type(peakDailyDemand),type(MaxDemandShaving))


    peak_demand_bar = px.bar( aggregated_df, x="Month", y=["PeakDailyDemand", "MaxDemandShaving"] ,
             title="Monthly Peak and Average Demand: " + buildingName,
             labels={"value": "Demand"},
             hover_name="Month", 
             hover_data=["MonthlyPeakDemand"],
             height=600,
              
            )

    peak_demand_bar.update_layout(
        legend=dict(orientation="h"),
        margin=dict(l=10, r=10, t=25, b=40)
        )  
    
    print("we are done with file creation")
    peak_demand_bar= peak_demand_bar.to_json(peak_demand_bar)
    
    # bar_graph_data=jsonify({"PeakDailyDemand":PeakDailyDemand,"MaxDemandShaving":MaxDemandShaving,
    #                 "buildingName":buildingName
    #                 })
  

    
#-------------------- End Create Pivots for 3D Graphs -----------------------------------------------'''


#'''---------------------- End Create Monthly Data DF ---------------------------------------------------------


#'''---------------------- Start Create BESS DF -------------------------------------------------------
def bess_filter(data):
    #create a dataframe to store ESS charging and discharging data
    dispatchSchedule = pd.DataFrame(columns=['Month','Energy','Duration','StartTime','EndTime','Charge','SOC'])
    currentMonth = []
    currentPeak = 0

    #loop through file to get data by month
    maxstateofCharge = 1
    maxESS = 0
    minSOC = -1
    dod = 1-((float( data['inputs']['depthDischarge']))/100)

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
    OMCost_kWh = float(data['inputs']['floatInput1'])
    OMCost_fixed = float( data['inputs']['floatInput2'])
    capitalCost_kWh =  float(  data['inputs']['floatInput3'])
    capitalCost_kW =   float( data['inputs']['floatInput4'])
    footprint_kWh = float(data['inputs']['footprint']) #in cm^2 using values from Tesla Megapack  

    # OMCost_kWh = 24.25
    # OMCost_fixed = 0
    # capitalCost_kWh = 967.50
    # capitalCost_kW = 0
    # footprint_kWh = 37 #in cm^2 using values from Tesla Megapack 

    #BESS variables
    #-----new BESS capacity variable: sets the recommended capacity to the BESS_capacity_rec vairable. This allows BESS_capaicty to be updated by users
    #-----uncomment the 2 lines below. Delete the old BESS_capacity = maxstateofCharge line ----
    BESS_capacity_rec = maxstateofCharge
    BESS_capacity = data['inputs']['bessCapacity']

    # BESS_capacity = maxstateofCharge
    power_duration =int( data['inputs']['selectInput']) # Use duration to calculate power based on BESS Capacity. N/A (0) uses maxpower needed to shave the peak
    if power_duration == 0:
        BESS_power = math.ceil(maxPeakDemandShaving)
    if power_duration > 0:
        BESS_power = math.ceil(BESS_capacity/power_duration)    
    BESS_cost = (OMCost_kWh * BESS_capacity + OMCost_fixed) + (capitalCost_kWh * BESS_capacity + capitalCost_kW * BESS_power)
    BESS_footprint = BESS_capacity * footprint_kWh

    #print statements
    print("Building: ", buildingName)
    print('BESS Capacity (kWh): ', BESS_capacity)
    print('BESS Power (kW): ', BESS_power)
    print("BESS Cost ($): ", BESS_cost)
    print("BESS Footprint (ft^2): ", BESS_footprint)

    return jsonify({'BESS_capacity':BESS_capacity,"BESS_power":BESS_power,"BESS_cost":BESS_cost,"BESS_footprint":BESS_footprint , "BESS_capacity_rec" : maxstateofCharge})

@app.route('/bess_calculation', methods=['POST'])
def bess_calculatiion():
    try:
        
        data=request.json
        print("here")
        print("data==>",data)
        calculation_output=bess_filter(data)
        return calculation_output
    
    except:
        print("exception occurs")
        data={'inputs': {'floatInput1': 24.25, 'floatInput2': 0, 'floatInput3': 967.5, 'floatInput4': 0, 'selectInput': 4, 'depthDischarge': 15, 'footprint': 37}}
        calculation_output=bess_filter(data)
        return calculation_output


#-------------------------End Create BESS DF -----------------------------------------------------------'''
'''
#------------------component: monthly load profile by date range ---------------------------

#Get date and time and combine into datetime variable
startDateLP = date(2019,1,1)
startTimeLP = time(00,00)
endDateLP = date(2019,1,1)
endTimeLP = time(23,59)
startDateTimeLP = dt.combine(startDateLP, startTimeLP)
endDateTimeLP = dt.combine(endDateLP, endTimeLP)

#filter the dateframe by the date range and set x and y variables
filtered_df = df[(df['Date'].dt.date >= startDateLP) & (df['Date'].dt.date <= endDateLP)]
xDateTime = filtered_df.loc[:,"Date"].values.astype('datetime64[m]') 
monthlyDemandData = filtered_df.loc[:,"Demand"].values

#create date plot and formatting
fig_LPbyDate = make_subplots(rows=1, cols=1)    
fig_LPbyDate.update_xaxes(tickformat="%m/%d \n%H:%M", title_text="Date")

fig_LPbyDate.update_layout(
    xaxis=dict(tickangle=-45),
    title= " Load Profile: " + buildingName + " \nDate Range: " + startDateTimeLP.strftime("%m/%d/%y %H:%M") + " - " + endDateTimeLP.strftime("%m/%d/%y %H:%M"),
    xaxis_title="Date",
    yaxis_title="Demand (kW)",
    legend=dict(orientation="h"),
    margin=dict(l=10, r=10, t=30, b=20),
    showlegend=False
)

fig_LPbyDate.add_trace(
    go.Scatter(x=xDateTime, y=monthlyDemandData, mode="lines")
)
#------------------component: monthly load profile by date range ---------------------------
'''
#-----------------------component: comp_3D_daily_plot----------------------------

@app.route('/give_comp_3D_daily_plot')
def give_comp_3D_daily_plot():
    print("3D Daily ROUTE")
    
    global x_daily,y_daily,z_daily
    # Create 3D surface graph data
    surface = go.Surface(
       z=z_daily, x=x_daily, y=y_daily
    )

    layout = go.Layout(scene=dict(xaxis_title='Hour',
    yaxis_title='Day of Week',
    zaxis_title='Demand',aspectmode="cube"),title=fig_daily_title,height=500,width=600)

    # Create a figure
    fig = go.Figure(data=[surface], layout=layout)

    # Convert the figure to JSON
    graph_json = fig.to_json()

    return jsonify(graph_json)

#----------------------component: comp_3D_monthly_plot----------------------------

@app.route('/give_comp_3D_monthly_plot')
def give_comp_3D_monthly_plot():
    print("3D MONTH ROUTE")
    # Create 3D surface graph data
    global x_monthly,z_monthly,y_monthly,fig_month_title
    surface = go.Surface(
       z=z_monthly, x=x_monthly, y=y_monthly
    )

    layout = go.Layout(scene=dict(xaxis_title='Hour',
    yaxis_title='Month',
    zaxis_title='Demand',aspectmode="cube"),title=fig_month_title,height=500,width=600)

    # Create a figure
    fig = go.Figure(data=[surface], layout=layout)

    # Convert the figure to JSON
    graph_json = fig.to_json()

    return jsonify(graph_json)
   

#---------------component: max daily avg load vs peak demand---------------------------------------

     
@app.route('/get_demand_plot_data')
def get_demand_plot_data():
    global peak_demand_bar
    # return jsonify(peak_demand_bar)
    print("rout for get data called")
    global bar_graph_data,peakMonthlyDemand,monthlyPeakDemandShaving,peakDailyDemand
    bar_graph_data["Month"]=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    bar_graph_data["MonthlyPeakDemand"]=([float(x) for x in peakMonthlyDemand])
    bar_graph_data[ "MaxDemandShaving"]= ([float(x) for x in monthlyPeakDemandShaving])
    bar_graph_data[ "PeakDailyDemand"]=([float(x) for x in peakDailyDemand])
   
    print("bar=>",bar_graph_data)
    # bar_graph_data=json.dumps(bar_graph_data)
    json_data = json.dumps(bar_graph_data)
    # bar_graph_data=jsonify(bar_graph_data)
    print("data for graph",json_data)
    
    return (json_data)

#------------------component: monthly load profile ---------------------------
def apply_filter(month_val,checkboxes):
        #Get data for the chosen month
        monthValue = month_val
        monthName = calendar.month_name[monthValue]
        currentMonthDataDF = df.loc[df["Date"].dt.month == monthValue]
        # if startdate & end_date:
        #     currentMonthDataDF = df[(df['date'] >= start_date) & (df['date'] <= end_date) ]
        print(currentMonthDataDF)
        xDateTime = currentMonthDataDF.loc[:,"Date"].values.astype('datetime64[m]') 
        # xDateTime = currentMonthDataDF.loc[:,"Date"]

        global fig_monthlyDemand
        # Create a subplot with one plot for all curves
        fig_monthlyDemand = make_subplots(rows=1, cols=1)    

        # Update x-axis date formatting
        fig_monthlyDemand.update_xaxes(tickformat="%m/%d %H:%M", title_text="Date")

        # Update layout
        fig_monthlyDemand.update_layout(
            xaxis=dict(tickangle=-45),
            title= monthName + " Load Profile: " + buildingName,
            xaxis_title="Date",
            yaxis_title="Demand (kW)",
            # legend=dict(orientation="v", xanchor="right", yanchor="bottom"),
            # legend=dict(orientation="h", xanchor="right", yanchor="bottom"),
            height=600,
            margin=dict(l=10, r=10, t=25, b=80),
            showlegend=True,
        #     annotations=[
        # dict(
        #     x=-1,
        #     y=-2,
        #     xref="paper",
        #     yref="paper",
        #     text="Your Custom Text",
        #     showarrow=False,
        #     font=dict(
        #         size=12,
        #         color="black"
        #     )
        # )
    # ]
        )

        
        # 15 Minute Demand Data Plot
        monthlyDemandData = currentMonthDataDF.loc[:,"Demand"].values
        fig_monthlyDemand.add_trace(
            go.Scatter(x=xDateTime, y=monthlyDemandData, mode="lines",
                        name="15 Minute Demand Data")
        )

        if checkboxes['option1']:
            # Peak Daily Avg Demand (yellow dashed)
            peakDailyAvgDemandData = peakDailyDemand[monthValue-1]
            fig_monthlyDemand.add_trace(
                go.Scatter(x=[min(xDateTime), max(xDateTime)],
                        y=[peakDailyAvgDemandData, peakDailyAvgDemandData],
                        mode="lines",
                        
                        name="Peak Daily Avg. Demand",
                        line=dict(color="yellow", dash="dash"))
            )
            fig_monthlyDemand.add_annotation(
            x=max(xDateTime),  # x-coordinate of the annotation
            y=peakDailyAvgDemandData,  # y-coordinate of the annotation
            text=f"Peak Daily Avg. Demand: {peakDailyAvgDemandData:.2f}",  # Text to display in the annotation with 2 decimal places
            showarrow=True,  # Show arrow pointing to the annotation
            arrowhead=1,  # Arrowhead style
            ax=0,  # Arrow's x-direction
            ay=-20,  # Arrow's y-direction
            font=dict(color="black")  # Text color
        )

            


        if checkboxes['option2']:
            # Monthly Avg Demand (green dashed)
            avgMonthlyDemandData = avgMonthlyDemand[monthValue-1]
            fig_monthlyDemand.add_trace(
                go.Scatter(x=[min(xDateTime), max(xDateTime)],
                        y=[avgMonthlyDemandData, avgMonthlyDemandData],
                        mode="lines",
                        name="Monthly Avg. Demand",
                        line=dict(color="green", dash="dash"))
            )

            # Add annotation for monthly average demand value
            fig_monthlyDemand.add_annotation(
                x=max(xDateTime),  # x-coordinate of the annotation
                y=avgMonthlyDemandData,  # y-coordinate of the annotation
                text=f"Monthly Avg. Demand: {avgMonthlyDemandData:.2f}",  # Text to display in the annotation with 2 decimal places
                showarrow=True,  # Show arrow pointing to the annotation
                arrowhead=1,  # Arrowhead style
                ax=0,  # Arrow's x-direction
                ay=-20,  # Arrow's y-direction
                font=dict(color="green")  # Text color
            )
          
    

        if checkboxes['option3']:
            # Peak Monthly Demand (red dashed)
            peakMonthlyDemandData = peakMonthlyDemand[monthValue-1]
            fig_monthlyDemand.add_trace(
                go.Scatter(x=[min(xDateTime), max(xDateTime)],
                        y=[peakMonthlyDemandData, peakMonthlyDemandData],
                        mode="lines",
                        name="Peak Demand",
                        line=dict(color="red", dash="dash"))
            )
            fig_monthlyDemand.add_annotation( x=max(xDateTime),  # x-coordinate of the annotation
            y=peakMonthlyDemandData,  # y-coordinate of the annotation
            text=f"Peak Demand: {peakMonthlyDemandData:.2f}",  # Text to display in the annotation
            showarrow=True,
            arrowhead=1,  # Arrowhead style
            ax=0,  # Arrow's x-direction
            ay=-20,  # Arrow's y-direction
            font=dict(color="red") 
            )

        return jsonify(fig_monthlyDemand.to_json())

@app.route('/monthly_demand_profile', methods=['POST'])
def monthly_demand_profile():
    try:
        
        data=request.json
        checkboxes=data['checkboxes']
        print("checkboxes==>",checkboxes)
        
        #we get default month 1
        month_val= int(data['selectedMonth'])
        print("selectedMonth=",month_val)

        if(month_val):
            output=apply_filter(month_val,checkboxes)
            
        else:
            output=apply_filter(1,checkboxes)
        return output
    
    except:
        checkboxes={}
        output=apply_filter(1,checkboxes)
        return output    


def apply_date_filter(startdate,end_date):
        #Get data for the chosen month
        # monthValue = month_val
        # monthName = calendar.month_name[monthValue]
        # currentMonthDataDF = df.loc[df["Date"].dt.month == monthValue]
        # if startdate & end_date:
        print("we are on date")
        print(startdate,end_date)
        startdate=startdate.replace('T',' ')
        end_date=end_date.replace('T',' ')
        # currentMonthDataDF = df.loc[df["Date"].dt.month == monthValue]
        print(df.dtypes)
        currentMonthDataDF = df[(df['Date'] >= startdate) & (df['Date'] <= end_date) ]
        # print(currentMonthDataDF.dytpes)
        print(currentMonthDataDF)
        xDateTime = currentMonthDataDF.loc[:,"Date"].values.astype('datetime64[m]') 
        # xDateTime = currentMonthDataDF.loc[:,"Date"]

        global fig_monthlyDemand
        # Create a subplot with one plot for all curves
        fig_monthlyDemand = make_subplots(rows=1, cols=1)    

        # Update x-axis date formatting
        fig_monthlyDemand.update_xaxes(tickformat="%m/%d %H:%M", title_text="Date")

        # Update layout
        fig_monthlyDemand.update_layout(
            xaxis=dict(tickangle=-45),
            title=  " Load Profile: " + buildingName,
            xaxis_title="Date",
            yaxis_title="Demand (kW)",
            # legend=dict(orientation="v", xanchor="right", yanchor="bottom"),
            # legend=dict(orientation="h", xanchor="right", yanchor="bottom"),
            height=600,
            margin=dict(l=10, r=10, t=25, b=80),
            showlegend=True,
       )

        

        # 15 Minute Demand Data Plot
        monthlyDemandData = currentMonthDataDF.loc[:,"Demand"].values
        fig_monthlyDemand.add_trace(
            go.Scatter(x=xDateTime, y=monthlyDemandData, mode="lines",
                        name="15 Minute Demand Data")
        )


        

        return jsonify(fig_monthlyDemand.to_json())

@app.route('/date_filter', methods=['POST'])
def date_filter():
    try:
        
        data=request.json
        print("this is data==>",data)
        if data['timeSelection']['from']:
            start_date=data['timeSelection']['from']
        else:
            start_date=0
        if data['timeSelection']['to']:
            end_date=data['timeSelection']['to']
        else:
            end_date=0
        
        
        output=apply_date_filter(start_date,end_date)
            
        
        return output
    
    except:
       
        output=apply_date_filter(start_date,end_date)
        return output   

# @app.route('/date_filter', methods=['POST'])
# def date_filter():
#     try:
#         global peak_demand_bar
#         # return jsonify(peak_demand_bar)
#         print("rout for get data called")
#         data=request.json
#         start_date=request.timeSelection['form']
#         end_date=request.timeSelection['to']
#         data_preprocessing_date(df,uid,start_date,end_date,start_time,end_time)
    
#     except:
         

#------------------------------------------End Build the Components ------------------------------------------'''

if __name__ == "__main__": 
    app.run(debug=True)