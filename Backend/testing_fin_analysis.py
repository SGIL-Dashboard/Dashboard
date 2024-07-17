import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import calendar
import os
import pathlib
import numpy as np
from scipy.integrate import trapz
import math




#user inputs
BESS_cost = 400000
OM_Cost = 967.5
BESS_capacity = 365
dod = 85
ESSCapacity = 365
avgDailyValue = 30
df = pd.read_excel('backend/data/Administration Building.xlsx')



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
#-------------------Start Loan Amortization ----------------------------------------------------------- 
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
#-------------------End Loan Amortization -----------------------------------------------------------
    
#-------------------Start Depreciation -----------------------------------------------------------
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
#-------------------End Depreciation -----------------------------------------------------------
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