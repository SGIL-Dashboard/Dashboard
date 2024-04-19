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
import numpy_financial as npf
from scipy.integrate import trapezoid
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
@app.route('/Fancial_Analysis', methods=['POST'])
def FA():
    filename = "Administration Building.xlsx"
    data_folder = "data"
    results_folder = "results"
    directory = pathlib.Path(__file__).parent.resolve()
    data_filepath = os.path.join(directory, data_folder, filename)
    file = pd.ExcelFile(data_filepath)
    df=file.parse("PyLoad")
    buildingName = filename.replace('PyLoad.xlsx','')

    #-------------------- End Get Data --------------------------------------------------------

    #-------------------- Start Create General DF ---------------------------------------------

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
                energy_under_curve = trapezoid(demandIntegrate, dateIntegrate_int)
                energy_under_line = trapezoid(currentPeakDemand * np.ones_like(demandIntegrate), dateIntegrate_int)
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
        print("dispatchSchedule: ", dispatchSchedule)
        essData = {}
        ESSCapacity = dispatchSchedule
        dispatchSchedule = pd.DataFrame(columns=['Month','Energy','Duration','StartTime','EndTime','Charge','SOC'])
        

    #cost variables (can possibly be set with filters)
    OMCost_kWh = 24.25
    OMCost_fixed = 0
    capitalCost_kWh = 967.50
    capitalCost_kW = 0
    footprint_kWh = 37 #in cm^2 using values from Tesla Megapack  
    sqcm_to_sqft = 0.00107639

    #BESS variables
    BESS_capacity_rec = maxstateofCharge
    BESS_capacity = 500
    power_duration = 4 # Use duration to calculate power based on BESS Capacity. N/A (0) uses maxpower needed to shave the peak
    if power_duration == 0:
        BESS_power = math.ceil(maxPeakDemandShaving)
    if power_duration > 0:
        BESS_power = math.ceil(BESS_capacity/power_duration)    
    BESS_cost =  capitalCost_kWh * BESS_capacity + capitalCost_kW * BESS_power
    OM_Cost = OMCost_kWh * BESS_capacity + OMCost_fixed
    BESS_footprint = math.ceil(BESS_capacity * footprint_kWh * sqcm_to_sqft)

    #print statements
    print("Building: ", buildingName)
    print('BESS Capacity (kWh): ', BESS_capacity)
    print('BESS Power (kW): ', BESS_power)
    print("BESS Cost ($): ", BESS_cost)
    print("BESS Footprint (ft^2): ", BESS_footprint)

    #-------------------------End Create BESS DF -----------------------------------------------------------'''


    #---------------------Start Financial Analysis Variables -------------------------------------------
    # inputsFormUser = request.json
    #user inputs
    project_length = 20
    initial_investment = 100000  
    debt_percent = 30 #loan rate
    debt_interest_rate = 6
    debt_term = 18 # loan term
    property_tax_rate = 3         
    property_assessed_pct = 100 #percent value (not decimal)  
    fed_tax_rate = 21      
    state_tax_rate = 7
    insurance_rate = 0.25
    # project_length = inputsFormUser['project_length']
    # initial_investment = inputsFormUser['initial_investment']  
    # debt_percent = inputsFormUser['debt_percent'] #loan rate
    # debt_interest_rate = inputsFormUser['debt_interest_rate']
    # debt_term = inputsFormUser['debt_term'] # loan term
    # property_tax_rate = inputsFormUser['property_tax_rate']         
    # property_assessed_pct = inputsFormUser['property_assessed_pct'] #percent value (not decimal)  
    # fed_tax_rate = inputsFormUser['fed_tax_rate']     
    # state_tax_rate = inputsFormUser['state_tax_rate']
    # insurance_rate = inputsFormUser['insurance_rate']
    # print("inputsFormUser",inputsFormUser)
    energy_payment = .25  #average energy rate utility
    demand_payment = 65  #average demand rate utility
    fixed_payment = 100 #monthly fixed amount utility
    reserve_interest = 1.5      
    reserve_percent = 10
    ITC_rate = 30 #ITC percent value (not decimal)
    #defaults. not entered by user
    # inputsFormUser = request.json







    federal_type_dep = 'MACRS'  #options are MACRS, line, none
    state_type_dep = 'line'     #options are MACRS, line, none
    discount_rate = 0.10
    BESS_cycle_life = 7000
    BESS_efficiency = .85
    #initial calculated values
    property_assessed_value = BESS_cost * property_assessed_pct/100
    property_tax_amount = property_assessed_value * property_tax_rate/100
    insurance_payment = BESS_cost*insurance_rate/100
    total_reserve_amount = reserve_percent/100*initial_investment
    reserve_interest_pymt = total_reserve_amount *reserve_interest/100
    total_debt_amount = debt_interest_rate/100*initial_investment
    effective_tax_rate_factor = state_tax_rate/100+fed_tax_rate/100*(1-state_tax_rate/100)
    ITC_basis = BESS_cost 
    deductable_expenses = OM_Cost + insurance_payment
    BESS_usable_capacity = BESS_capacity * (1-dod)
    total_energy_dispatched_kWh = BESS_usable_capacity * BESS_cycle_life * BESS_efficiency
    ITC_amount = ITC_basis*ITC_rate/100 

    #---------------------End Financial Analysis Variables -------------------------------------------

    #---------------------Start Create Financial Analysis DF -----------------------------------------------

    # Define the labels for the rows and columns

    rows = ['Cash Flow', 'Cummulative Cash Flow','DR Capacity Revenue', 'Bill Savings','OM Expense', 'Insurance', 'Property Tax', 'EBITDA', 'Debt', 'Principal', 'Depreciation_Rate_State','Depreciation_Rate_Federal','State Tax', 'Fed Tax']
    columns = list(range(project_length+1))  # Years 0 through 20

    financial_data = np.zeros((len(rows), len(columns)))  # Using zeros as placeholder values

    financial_df = pd.DataFrame(financial_data, index=rows, columns=columns)

    #print('financial df:', financial_df)

    #---------------------End Cerate Financial Analysis DF -------------------------------------------------

    #------------------------Start Utility Bill Calc DF ----------------------------------------------
    energy_before = df.groupby(["Year", "Month"])["Demand"].sum() / 4
    energy_after = ESSCapacity.groupby(["Month"])["Energy"].sum() *-1/15
    peak_demand_before = df.groupby(["Year", "Month"])["Demand"].max()
    peak_demand_after = avgDailyValue.groupby(["Year","Month"])["dailyAvgDemand"].aggregate(maxAvgDemand = 'max')

    Usage = pd.DataFrame(index=energy_before.index.levels[1]) 

    # Adding the calculated values to 'Usage' DataFrame
    Usage['Energy_Before'] = energy_before.values
    Usage['Energy_After'] = energy_after.reindex(Usage.index, fill_value=0).values  # Reindex to match 'Usage' and fill NaN with 0
    Usage['Peak_Demand_Before'] = peak_demand_before.values
    Usage['Peak_Demand_After'] = peak_demand_after.values

    # Resetting index to have Month as a column
    Usage.reset_index(inplace=True)
    Usage.rename(columns={"index": "Month"}, inplace=True)

    #------------------------End Utility Bill Calc DF ----------------------------------------------

    #-------------------- Start Bill Savings ---------------------------------------------------

    def calculate_utility_bill_savings(Usage, energy_payment, demand_payment, fixed_payment):
        # Calculate original and increased yearly energy costs
        Usage['Energy_Before_Cost'] = Usage['Energy_Before'] * energy_payment
        Usage['Energy_After_Cost'] = Usage['Energy_After'] * energy_payment + Usage['Energy_Before_Cost']
        
        # Calculate original and new peak demand costs
        Usage['Peak_Demand_Before_Cost'] = Usage['Peak_Demand_Before'] * demand_payment
        Usage['Peak_Demand_After_Cost'] = Usage['Peak_Demand_After'] * demand_payment
        
        # Calculate the original and new bills per month
        Usage['Original_Bill'] = Usage['Energy_Before_Cost'] + Usage['Peak_Demand_Before_Cost'] + fixed_payment
        Usage['New_Bill'] = Usage['Energy_After_Cost'] + Usage['Peak_Demand_After_Cost'] + fixed_payment
        
        # Calculate the monthly savings
        Usage['Monthly_Savings'] = Usage['Original_Bill']  - Usage['New_Bill']
        
        # Calculate the total annual savings
        Total_Savings = Usage['Monthly_Savings'].sum()
        Total_Orignal_Bill = Usage['Original_Bill'].sum()
        Total_New_Bill = Usage['New_Bill'].sum()
        
        return Total_Orignal_Bill, Total_New_Bill, Total_Savings

    #energy_payment = 0.12 
    #demand_payment = 15    
    #fixed_payment = 100    

    #bill_details, annual_savings = calculate_utility_bill_savings(Usage, energy_payment, demand_payment, fixed_payment)

    #print("bill details: ", bill_details)
    #print("annual savings: ", annual_savings)
    #bill_details, annual_savings

    #-------------------- End Bill Savings ---------------------------------------------------

    #'''-------------------Start Loan Amortization ----------------------------------------------------------- 
    def loan_amortization_calculator(total_debt_amount, debt_interest_rate, debt_term):
        monthly_interest_rate = debt_interest_rate / 12 / 100  # Convert annual rate to monthly and percentage to decimal
        total_payments = debt_term * 12

        # Calculate monthly payment
        monthly_payment = (monthly_interest_rate * total_debt_amount) / (1 - (1 + monthly_interest_rate) ** -total_payments)

        current_balance = total_debt_amount
        amortization_schedule = []

        yearly_payment_summary = {
            'Yearly Payment': 0,
            'Yearly Interest': 0,
            'Yearly Principal': 0,
        }

        for payment_number in range(1, total_payments + 1):
            interest_payment = current_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            current_balance -= principal_payment

            yearly_payment_summary['Yearly Payment'] += monthly_payment
            yearly_payment_summary['Yearly Interest'] += interest_payment
            yearly_payment_summary['Yearly Principal'] += principal_payment

            if payment_number % 12 == 0 or payment_number == total_payments:  # End of year or last payment
                amortization_schedule.append({
                    'Year': payment_number // 12,
                    'Yearly Payment': yearly_payment_summary['Yearly Payment'],
                    'Yearly Interest': yearly_payment_summary['Yearly Interest'],
                    'Yearly Principal': yearly_payment_summary['Yearly Principal'],
                    'Remaining Balance': current_balance if current_balance > 0 else 0
                })
                # Reset yearly summaries
                yearly_payment_summary = {
                    'Yearly Payment': 0,
                    'Yearly Interest': 0,
                    'Yearly Principal': 0,
                }

            if current_balance <= 0:
                break

        return amortization_schedule
    

    loanAmortization = loan_amortization_calculator(total_debt_amount, debt_interest_rate, debt_term)


    for payment in loanAmortization:
        print(payment)
    #-------------------End Loan Amortization -----------------------------------------------------------'''
        
    #'''-------------------Start Depreciation -----------------------------------------------------------
    def get_depreciation_schedule(federal_type_dep, state_type_dep):
        macrs_5_year = [20, 32, 19.2, 11.52, 11.52, 5.76]  # Simplified 5-year MACRS percentages

        def calculate_straight_line(years):
            return [100 / years] * years  # Evenly spread over the years

        def calculate_depreciation(depreciation_type):
            if depreciation_type == 'MACRS':
                return macrs_5_year
            elif depreciation_type == 'line':
                return calculate_straight_line(7)  # Assuming a 5-year period for straight-line as well
            elif depreciation_type == 'none':
                return [0] * 5  # No depreciation for 5 years
            else:
                raise ValueError("Invalid depreciation type. Choose '5 yr MACRS', 'straight line', or 'no depreciation'.")

        federal_schedule = calculate_depreciation(federal_type_dep)
        state_schedule = calculate_depreciation(state_type_dep)

        schedule = []
        for year in range(1, max(len(federal_schedule), len(state_schedule)) + 1):
            schedule.append({
                'Year': year,
                'Federal Depreciation (%)': federal_schedule[year - 1] if year <= len(federal_schedule) else 0,
                'State Depreciation (%)': state_schedule[year - 1] if year <= len(state_schedule) else 0
            })

        return schedule


    schedule = get_depreciation_schedule(federal_type_dep, state_type_dep)



    for year_info in schedule:
        print(year_info)
    #-------------------End Depreciation -----------------------------------------------------------'''
    #-----------------------Start Capacity Payment --------------------------------------------------
    #----------------------------      $/kW/mo   # of mo -------------------------------------------------
    #Reservation Calc SCR (summer)	    31.38	    6
    #Reservation Calc SCR (winter)	    32.20	    6
    #Reservation Calc CSRP	            18.00	    5
    #Reservation Calc DLRP (Tier 2)	    5.00	    5
    def capacity_payment_calc():
        return 0
    #----------------------End Capacity Payment ----------------------------------------------    
    #-----------------------Start Payback Calc --------------------------------------------------
    # rows = ['Cash Flow', 'Cummulative Cash Flow','DR Capacity Revenue', 'Bill Savings','OM Expense', 'Insurance', 'Property Tax', 'EBITDA', 'Interest', 'Principal',  'Depreciation','State Tax', 'Fed Tax']    
    def calculate_payback(project_length,debt_term, financial_df):
        cash_flow = 0
        cummulative_cash_flow = 0
        DR_capacity_revenue = 0
        bill_savings = 0
        OM_expense = 0
        insurance_expense = 0 
        EBITDA_calc = 0
        interest_expense = 0
        principal_expense = 0
        depreciation_rate_state = 0
        depreciation_rate_fed = 0
        depreciation_basis = 0
        depreciation_amount_state = 0
        depreciation_amount_fed = 0
        state_deductions = 0
        default_val = {'Federal Depreciation (%)': 0, 'State Depreciation (%)': 0}
        state_tax = 0
        fed_tax = 0
    
        for i in range(0, project_length):
            if i == 0:
                cash_flow = -(initial_investment + total_reserve_amount)
                cummulative_cash_flow = cash_flow

                #populate the data frame for year 0
                financial_df.loc['Cash Flow', i] = cash_flow
                financial_df.loc['Cummulative Cash Flow', i] = cummulative_cash_flow

            elif i > 0 and i < debt_term:
                bill_savings = calculate_utility_bill_savings(Usage, energy_payment, demand_payment, fixed_payment)[2]
                capacity_payment = capacity_payment_calc()
                OM_expense = OM_Cost
                insurance_expense = insurance_payment 
                EBITDA_calc = (bill_savings + capacity_payment + reserve_interest_pymt) - (OM_expense + insurance_expense)
                annual_PI_calc = loan_amortization_calculator(total_debt_amount, debt_interest_rate, debt_term)[i]
                interest_expense = annual_PI_calc['Yearly Interest']
                principal_expense = annual_PI_calc['Yearly Principal']
                annual_depreciation_calc = get_depreciation_schedule(federal_type_dep, state_type_dep)[i] if i< len(get_depreciation_schedule(federal_type_dep, state_type_dep)) else default_val
                depreciation_rate_fed = annual_depreciation_calc['Federal Depreciation (%)']
                depreciation_rate_state = annual_depreciation_calc['State Depreciation (%)']
                depreciation_basis = ITC_basis - (.5*ITC_rate/100*ITC_basis) if depreciation_rate_fed != 0 else 0
                depreciation_amount_state = depreciation_basis * depreciation_rate_state/100
                depreciation_amount_fed = depreciation_basis * depreciation_rate_fed/100
                state_deductions = depreciation_amount_state + OM_expense + insurance_expense
                state_taxable_rev = capacity_payment + reserve_interest_pymt
                state_taxable_income_less_deductions = state_taxable_rev - state_deductions
                state_tax_liability = -(state_taxable_income_less_deductions * state_tax_rate/100)
                pre_tax_cash_flow = -(OM_Cost+ principal_expense+interest_expense+insurance_expense)
                after_tax_value_of_energy = bill_savings*(1-(state_tax_rate/100+(1-state_tax_rate/100)*fed_tax_rate/100)) if depreciation_rate_fed != 0 else bill_savings
                fed_taxable_rev = capacity_payment + reserve_interest_pymt
                fed_deductions = depreciation_amount_fed + OM_expense + insurance_expense + -state_tax_liability
                fed_taxable_income_less_deductions = fed_taxable_rev - fed_deductions
                fed_tax_liability = -(fed_taxable_income_less_deductions * fed_tax_rate/100)
                after_tax_annual_cost = pre_tax_cash_flow + state_tax_liability + fed_tax_liability
                after_tax_cash_flow = after_tax_annual_cost + after_tax_value_of_energy + reserve_interest_pymt
                cash_flow_payback = after_tax_cash_flow + interest_expense * (1-effective_tax_rate_factor)+principal_expense
                cummulative_cash_flow = cash_flow_payback + financial_df.loc['Cummulative Cash Flow', i-1]
                
                #populate the data frame for year i
                financial_df.loc['Cash Flow', i] = cash_flow_payback
                financial_df.loc['Cummulative Cash Flow', i] = cummulative_cash_flow
                financial_df.loc['DR Capacity Revenue', i] = capacity_payment
                financial_df.loc['Bill Savings', i] = bill_savings
                financial_df.loc['OM Expense', i] = OM_expense
                financial_df.loc['Insurance', i] = insurance_expense 
                financial_df.loc['Property Tax', i] = property_tax_amount
                financial_df.loc['EBITDA', i] = EBITDA_calc
                financial_df.loc['Debt', i] = interest_expense
                financial_df.loc['Principal', i] = principal_expense
                financial_df.loc['Depreciation_Rate_State', i] = depreciation_rate_state
                financial_df.loc['Depreciation_Rate_Federal', i] = depreciation_rate_fed
                financial_df.loc['State Tax', i] = state_tax_liability
                financial_df.loc['Fed Tax', i] = fed_tax_liability
            elif i > debt_term:
                cash_flow = initial_investment + total_reserve_amount
                cummulative_cash_flow = cash_flow
                DR_capacity_revenue = 0
                bill_savings = 0
                OM_expense = 0
                insurance_expense = 0 
                EBITDA_calc = 0
                interest_expense = 0
                principal_expense = 0
                state_tax = 0
                fed_tax = 0
        return financial_df


    project_cashflows = calculate_payback(project_length,debt_term, financial_df)
    project_cashflows.to_excel(os.path.join(directory, results_folder, "project_cashflows.xlsx"), index=True)

    yearly_cash_flows = project_cashflows.iloc[0].values
    cumulative_cash_flow = project_cashflows.iloc[1].values
    npv = npf.npv(discount_rate, [initial_investment] + yearly_cash_flows)
    irr = npf.irr([initial_investment] + yearly_cash_flows)
    payback_period = np.where(cumulative_cash_flow > 0)[0][0]  
    total_lifecycle_costs = -np.sum([initial_investment] + yearly_cash_flows)  # Total costs (negative sign for cash out)
    lcoe = total_lifecycle_costs / total_energy_dispatched_kWh  # Cost per kWh
    bill_savings_yr1 = project_cashflows.iloc[3,1]
    dr_rev_yr1 = project_cashflows.iloc[2,1]
    print(request.json)
    print("\n npv: ", npv, "\n irr: ", irr, "\n payback_period: ", payback_period, "\n lcoe: ", lcoe, "\n itc: ", ITC_amount, "\n year 1 bill savings: ", bill_savings_yr1, "\n demand response capacity revenue: ", dr_rev_yr1 )
    # return jsonify({'message':"success", 'npv':npv, 'irr':irr, 'payback_period':payback_period, 'lcoe':lcoe, 'itc':ITC_amount, 'year1_bill_savings':bill_savings_yr1, 'dr_capacity_revenue':dr_rev_yr1, 'project_cashflows':project_cashflows.to_json()})
    print('\n project_cashflows: \n', project_cashflows)
    return jsonify({"message" : "success" , "npv" : int(npv) ,"irr" : int(irr) , "payback_period" : int(payback_period) , "lcoe" : int(lcoe) , "itc" : int(ITC_amount) , "year1_bill_savings" : int(bill_savings_yr1) , "dr_capacity_revenue" : int(dr_rev_yr1) })

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