import React, { useState } from "react";
import Loader from "../Loader/Loader";
import { stylings } from "../../UTILS/UTILS_STYLES";
import { globalContext } from "../../Context/Context";
import RenderForm from "./RenderForm";
import SVGComponent from "../SVGS/SVGS";
import { makeApiRequest } from "../../UTILS/UTILS_HELPERS";
import toast from "react-hot-toast";
import Results from "./Results";
export default function FinancialAnalysis({ bessCost  , bessPower}) {
  const { theme } = React.useContext(globalContext);
  const errorsInitialState = {
    projectDebt: {
      debt_percent: false,
      debt_term : false,
      debt_interest_rate: false
    },
    reserveAccounts: {
      reserveAmount: false,
      interestRate: false

    },
    utilityBill: {
      averageDemandRate: false,
      averageEnergyRate: false,
      monthlyFixedAmount: false
    },
    initialInvestment:
    {
      project_length: false,
      bessCost: false,
      differential: false,
      initial_investment: false
    },
    investmentTaxCredit: {
      fedral: false,

    },
    taxes: {
      fed_tax_rate: false,
      state_tax_rate: false,
      insurance_rate: false,
      salesTax: false,
      property_tax_rate : false,
      AssedssedValue: false,
      property_assessed_pct: false,
    },
    capacityPayments: {
      commitmentAmount: false,
      commitmentPayment: false
    }
  }
  const [results, setResults] = React.useState({ npv: 100000, irr: 14, payback_period: 4, lcoe: 0.15, itc: 145125, bill_savings_yr1: 29825, dr_rev_yr1: 34850 });
  const renderResultsHelper = [
    {
      label: "Payback Time", accessor: "payback_period" , backLabel : " Years"
    },
    {
      label: "NPV", accessor: "npv"
    },
    {
      label: "DR Revenue", accessor: "dr_rev_yr1"
    },
    {
      label: "IRR", accessor: "irr" , backLabel : " / %"
    },
    {
      label: "ITC", accessor: "itc"
    },
    {
      label: "1 Year Bill Savings", accessor: "bill_savings_yr1"
    },
    {
      label: "LCOE", accessor: "lcoe" , backLabel : " $/kWh"
    },

  ]
  const [selectedForm , setSelectedForm] = useState();
  const [errors, setErrors] = React.useState(JSON.parse(JSON.stringify(errorsInitialState)));
  const [state, setState] = React.useState({
    differential: "",
    projectDebt: {
      debt_percent : { value: 30, selectedMeasureUnit: "%" },
      debt_term : 18,
      debt_interest_rate: 6,
    },
    initialInvestment: {
      project_length: { value: 20, selectedMeasureUnit: "years" },
      bessCost: bessCost,
      differential: { value: 30, selectedMeasureUnit: "$" },
      initial_investment: bessCost + 1300
    },
    reserveAccounts: {
      reserveAmount: { value: 30, selectedMeasureUnit: "%" },
      interestRate: 1.5
    },
    utilityBill: {
      averageDemandRate: 20,  
      averageEnergyRate: 5,
      monthlyFixedAmount: 200
    },
    investmentTaxCredit: {
      fedral: {
        value: 30,
        selectedMeasureUnit: "%"
      },
    },
    taxes: {
      fed_tax_rate: 21,
      state_tax_rate: 7,
      insurance_rate: 0.25,
      salesTax: 8,
      property_tax_rate : 3,
      AssedssedValue: 4000,
      property_assessed_pct: 100,
    },
    capacityPayments: {
      commitmentAmount: { value: 30, selectedMeasureUnit: "%" },
      commitmentPayment: { value: 30, selectedMeasureUnit: "kW" },
    },
    demandResponse : {
      inputs : 
      {
        January : {CommitmentAmount : 50 , CommitmentPayment : 43 , totalDrPayment : 2150},
        February : {CommitmentAmount : 50 , CommitmentPayment : 43 , totalDrPayment : 2150},
        March : {CommitmentAmount : 50 , CommitmentPayment : 43 , totalDrPayment : 2150},
        April : {CommitmentAmount : 50 , CommitmentPayment : 43 , totalDrPayment : 2150},
        May : {CommitmentAmount : 50 , CommitmentPayment : 143 , totalDrPayment : 7150},
        June : {CommitmentAmount : 50 , CommitmentPayment : 43 , totalDrPayment : 2150},
        July : {CommitmentAmount : 50 , CommitmentPayment : 43 , totalDrPayment : 2150},
        August : {CommitmentAmount : 50 , CommitmentPayment : 43 , totalDrPayment : 2150},
        September : {CommitmentAmount : 50 , CommitmentPayment : 43 , totalDrPayment : 2150},
        October : {CommitmentAmount : 50 , CommitmentPayment : 43 , totalDrPayment : 2150},
        November : {CommitmentAmount : 50 , CommitmentPayment : 43 , totalDrPayment : 2150},
        December : {CommitmentAmount : 50 , CommitmentPayment : 143 , totalDrPayment : 7150},
      },
      selectedCommetmentAmount : "%"
    }
  });
  React.useEffect(() => {
    setState({ ...state, initialInvestment: { ...state.initialInvestment, bessCost: bessCost, totalInitialInvestment: bessCost + 1300 } });
  }, [bessCost])
  React.useEffect(() => {
    const demandResponse = state.demandResponse.inputs;
    Object.keys(demandResponse).map((val) => 
    {
      if(state.demandResponse.selectedCommetmentAmount === "%")
      {
        demandResponse[val].totalDrPayment = ((demandResponse[val].CommitmentAmount/100) * bessPower) * demandResponse[val].CommitmentPayment;
      }
      else
      {
        demandResponse[val].totalDrPayment = demandResponse[val].CommitmentAmount * demandResponse[val].CommitmentPayment;
      }
    })
    setState({ ...state, initialInvestment: { ...state.initialInvestment, bessCost: bessCost, totalInitialInvestment: bessCost + 1300 }  , demandResponse : { ...state.demandResponse , inputs : {...demandResponse}}});
  }, [bessPower])
  const [formHelpers, setFormHelpers] = React.useState(
    {
      projectDebt: {
        label: "Project Debt",
        accessor: "projectDebt",
        fields: [
          {
            label: "DEBT Amount",
            accessor: "debt_percent",
            multipleMeasureUnits: ["%", "$"],
          },
          { label: "Loan Term", accessor: "debt_term " },
          { label: "Loan Rate", accessor: "debt_interest_rate" },
        ],
      },
      initialInvestment: {
        label: "Total Initial Investment",
        accessor: "initialInvestment",
        fields: [
          {
            label: "Project Length",
            accessor: "project_length",
            multipleMeasureUnits: ["Days", "Years"],
          },
          {
            label: "BESS Cost",
            accessor: "bessCost",
            readOnly: true,
          },
          {
            label: "Differential",
            accessor: "differential",
            multipleMeasureUnits: ["%", "$"],
          },
          {
            label: "Total",
            accessor: "initial_investment",
            readOnly: true,
          }
        ]
      },
      reserveAccounts: {
        label: "Reserve Accounts",
        accessor: "reserveAccounts",
        fields: [
          {
            label: "Reserve Amount",
            accessor: "reserveAmount",
            multipleMeasureUnits: ["%", "$"]
          },
          {
            label: "Interest Rate",
            accessor: "interestRate"
          }
        ]
      },
      utilityBill: {
        label: "Utility Bill",
        accessor: "utilityBill",
        fields: [
          {
            label: "Average Demand Rate",
            accessor: "averageDemandRate"
          },
          {
            label: "Average Energy Rate",
            accessor: "averageEnergyRate"
          },
          {
            label: "Monthly Fixed Amount",
            accessor: "monthlyFixedAmount"
          }
        ]
      },
      investmentTaxCredit: {
        label: "Investment Tax Credit",
        accessor: "investmentTaxCredit",
        fields: [
          {
            label: "Fedral",
            accessor: "fedral",
            multipleMeasureUnits: ["%", "$"]
          },
        ]
      },
      taxes: {
        label: "Taxes",
        accessor: "taxes",
        fields: [
          {
            label: "Fedral Income Tax",
            accessor: "fed_tax_rate"
          },
          {
            label: "State Income Tax",
            accessor: "state_tax_rate"
          },
          {
            label: "Insurance Rate",
            accessor: "insurance_rate"
          },
          {
            label: "Sales Tax",
            accessor: "salesTax"
          },
          {
            label: "Property Tax",
            accessor: "property_tax_rate "
          },
          {
            label: "Assessed Value",
            accessor: "AssedssedValue"
          },
          {
            label: "Assessed Percent",
            accessor: "property_assessed_pct"
          }
        ]
      },
      capacityPayments: {
        label: "Capacity Payments",
        accessor: "capacityPayments",
        fields: [
          {
            label: "Commitment Amount",
            accessor: "commitmentAmount",
            multipleMeasureUnits: ["%", "kW"]
          },
          {
            label: "Commitment Payment",
            accessor: "commitmentPayment",
            multipleMeasureUnits: ["kW", "$"]
          }
        ]
      },
      demandResponse: {
        label: "Demand Response",
        accessor: "demandResponse",
        fields: [
          {
            label: "January",
            accessor: "January"
          },
          {
            label: "February",
            accessor: "February"
          },
          {
            label: "March",
            accessor: "March"
          },
          {
            label: "April",
            accessor: "April"
          },
          {
            label: "May",
            accessor: "May"
          },
          {
            label: "June",
            accessor: "June"
          },
          {
            label: "July",
            accessor: "July"
          },
          {
            label: "August",
            accessor: "August"
          },
          {
            label: "September",
            accessor: "September"
          },
          {
            label: "October",
            accessor: "October"
          },
          {
            label: "November",
            accessor: "November"
          },
          {
            label: "December",
            accessor: "December"
          }
        ]
      }
    },

  );
  const [selectedParameters, setSelectedParameters] = React.useState([]);
  const parameters = [
    { label: "Total Initial Investment", accessor: "initialInvestment" },
    { label: "Project Debt", accessor: "projectDebt" },
    { label: "Reserve Accounts", accessor: "reserveAccounts" },
    { label: "Utility Bill", accessor: "utilityBill" },
    { label: "Investment Tax Credit", accessor: "investmentTaxCredit" },
    { label: "Taxes", accessor: "taxes" },
    { label: "Capacity Payments", accessor: "capacityPayments" },
    { label: "Demand Response", accessor: "demandResponse" }
  ];
  const handleClick = (value , makeSelection) => {
    const existingParameters = new Set(selectedParameters);
    if (!makeSelection) {
      existingParameters.delete(value);
      if(selectedForm === value)
      {
        setSelectedForm(undefined);
      }
    }
    else {
      existingParameters.add(value);
      setSelectedForm(value);
    }
    setSelectedParameters([...existingParameters]);
  }
  const handleSubmit = () => {
    let errors = JSON.parse(JSON.stringify(errorsInitialState));
    let foundError = false;
    selectedParameters.map((val) => {
      const currentState = { ...state[val] };
      const fields = formHelpers[val].fields;
      fields.map((feild) => {
        const value = currentState[feild.accessor];
        if (typeof value === "object") {
          if (value.value === "") {
            foundError = true;
            errors = { ...errors, [val]: { ...errors[val], haveError: true, [feild.accessor]: true } }
          }
        }
        else {
          if (value === "") {
            foundError = true;
            errors = { ...errors, [val]: { ...errors[val], haveError: true, [feild.accessor]: true } }
          }
        }
      })
    });
    setErrors(errors);
    if (!foundError) {
      const payload = {};
      selectedParameters.map((val) => {
        payload[val] = { ...state[val] };
      })
      makeApiRequest({ method: "post", urlPath: "Financial_analysis", body: payload })
    }
    else {
      toast.error("Please fill all the fields");
    }
  }
  return (
    <div className=" w-full h-fit py-[2rem] shrink-0 flex flex-col items-center gap-[4rem] justify-start changebg">
      {!bessCost ? (
        <div className="w-full h-[30rem] flex items-center justify-center">
          <Loader />
        </div>
      ) : (
        <>
          <span className=" w-full text-center text-[2rem] text-slate-400 font-bold pt-[1.5rem]">
            Financial Analysis
          </span>
          <div className=" w-full flex items-start justify-start">
            <div className=" w-[25%] pt-[1rem] ml-[2rem] shrink-0 flex flex-col items-center">
              <span className=" text-[1.3rem] w-full bg-slate-100 py-[.5rem] text-slate-400 font-semibold">Select Parameters</span>
              {parameters.map((val) => {
                return <div  className={selectedParameters.includes(val.accessor) ? " w-full border-b-[0.05rem] border-blue-900 flex items-center  bg-slate-200 justify-between" : " w-full border-b-[0.05rem] border-blue-900 bg-slate-100 flex items-center  hover:bg-slate-200 justify-between"}>
                  <button onClick={() => {
                  handleClick(val.accessor , true);
                }} className=" text-[1.2rem] py-[.4rem] flex-grow text-slate-700">{val.label}</button>
                  {selectedParameters.includes(val.accessor) ? <><button className=" pr-[0.2rem]" onClick={() => {
                    if(selectedForm === val.accessor)
                    {
                      setSelectedForm(undefined);
                    }
                    else
                    {
                      setSelectedForm(val.accessor);
                    }
                }}><SVGComponent selector={val.accessor=== selectedForm ? "eyeOpened" : "eyeClosed"} width={"w-[1.5rem]"} color={val.accessor === selectedForm ? "#1E3A8A" : "#9CA3AF"} /></button><button className=" pr-[0.2rem]" onClick={() => {
                  handleClick(val.accessor , false);
                }}><SVGComponent selector={"boldCross"} width={"w-[1.5rem]"} color="#1E3A8A" /></button></> : <></>}
                </div>
              })}
              <button onClick={() => {
                handleSubmit();
              }} className=" w-full h-[3rem] flex items-center justify-center shrink-0 mt-[2rem] text-[1.4rem] text-blue-900 border-[0.1rem] border-blue-900 rounded-full">Calculate</button>
            </div>
            <Results results={results} renderResultsHelper={renderResultsHelper} />
            {selectedForm ? <RenderForm bessPower = {bessPower} errors={errors[selectedForm]} val={selectedForm} formHelper={formHelpers[selectedForm]} state={state} setState={setState}/> : <div className=" w-[30%] flex flex-col items-center justify-center">
              <SVGComponent selector="select" width="w-[5rem]" color="#94A3B8"/>
              <span className=" text-[1.5rem] text-slate-400 font-semibold">Please Select a Parameter</span>
            </div>}
          </div>
          <div className=" w-full mt-[4rem] h-fit flex items-start justify-evenly">
          </div>
        </>
      )}
    </div>
  );
}