#import all the modules
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask
import dash_bootstrap_components as dbc
import json


import pandas as pd
from datetime import datetime as dt
from datetime import date, time
from datetime import timedelta
import calendar
import os
import pathlib
import numpy as np
import numpy_financial as npf
from scipy.integrate import trapezoid
import math


import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
energy_payment = .25  #average energy rate utility
demand_payment = 65  #average demand rate utility
fixed_payment = 100 #monthly fixed amount utility
reserve_interest = 1.5  
reserve_percent = 10
ITC_rate = 30 #ITC percent value (not decimal)

#defaults. not entered by user
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

print("\n npv: ", npv, "\n irr: ", irr, "\n payback_period: ", payback_period, "\n lcoe: ", lcoe, "\n itc: ", ITC_amount, "\n year 1 bill savings: ", bill_savings_yr1, "\n demand response capacity revenue: ", dr_rev_yr1 )


print('\n project_cashflows: \n', project_cashflows)
#----------------------End Payback Calc ----------------------------------------------    