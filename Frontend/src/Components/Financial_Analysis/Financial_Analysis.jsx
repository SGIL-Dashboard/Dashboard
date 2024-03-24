import React from "react";
import Loader from "../Loader/Loader";
import { stylings } from "../../UTILS/UTILS_STYLES";
import { globalContext } from "../../Context/Context";
import RenderForm from "./RenderForm";
import SVGComponent from "../SVGS/SVGS";
import { makeApiRequest } from "../../UTILS/UTILS_HELPERS";
import toast from "react-hot-toast";
import Results from "./Results";
export default function FinancialAnalysis({ bessCost }) {
  const { theme } = React.useContext(globalContext);
  const errorsInitialState = {
    projectDebt : {
      debtAmount : false,
      loanTerm : false,
      loanRate : false
    },
    reserveAccounts : {
      reserveAmount : false,
      interestRate : false
    
    },
    utilityBill : {
      averageDemandRate : false,
      averageEnergyRate : false,
      monthlyFixedAmount : false
    
    },
    initialInvestment : 
    {
      project_length : false,
      bessCost : false,
      differential : false,
      totalInitialInvestment : false
    },
    investmentTaxCredit : {
      fedral : false,
    
    },
    taxes : {
      fedralIncomeTax : false,
      stateIncomeTax : false,
      insuranceRate : false,
      salesTax : false,
      propertyTax : false,
      AssedssedValue : false,
    },
    capacityPayments : {
      commitmentAmount : false,
      commitmentPayment : false
    }
 }
 const [results , setResults] = React.useState({npv : 100000 , irr : 14 , payback_period : 4 , lcoe : 0.15 , itc : 145125 , bill_savings_yr1 : 29825 ,  dr_rev_yr1 : 34850});
 const renderResultsHelper = [
  {
    label : "NPV" , accessor : "npv"
  },
  {
    label : "Demand Response Revenue" , accessor : "dr_rev_yr1"
  },
  {
    label : "IRR" , accessor : "irr"
  },
  {
    label : "Payback" , accessor : "payback_period"
  },
  {
    label : "ITC" , accessor : "itc"
  },
  {
    label : "1 year bill savings" , accessor : "bill_savings_yr1"
  },
  {
    label : "LCOE" , accessor : "lcoe"
  },

 ]
 const formRenderingOrder = ["initialInvestment" ,  "taxes" , "utilityBill" , "reserveAccounts" , "investmentTaxCredit" , "capacityPayments" , "projectDebt"]
  const [errors , setErrors] = React.useState(JSON.parse(JSON.stringify(errorsInitialState)));
  const [state, setState] = React.useState({
    differential: "",
    projectDebt: {
      debtAmount: { value : 30 , selectedMeasureUnit: "%" },
      loanTerm: 18,
      loanRate: 5,
    },
    initialInvestment : {
      project_length : {value : 20 , selectedMeasureUnit : "years"},
      bessCost : bessCost,
      differential : {value : 30 , selectedMeasureUnit : "$"},
      totalInitialInvestment : bessCost + 1300
    },
    reserveAccounts : {
      reserveAmount : {value : 30 , selectedMeasureUnit : "%"},
      interestRate : 1.5
    },
    utilityBill : {
      averageDemandRate : 20,
      averageEnergyRate : 5,
      monthlyFixedAmount : 200
    },
    investmentTaxCredit : {
      fedral : {
       value : 30,
        selectedMeasureUnit : "%"
      },
    },
    taxes : {
      fedralIncomeTax : 21,
      stateIncomeTax : 7,
      insuranceRate : 0.25,
      salesTax : 8,
      propertyTax : 2,
      AssedssedValue : 4000,
      AssedssedPercent : 100,
    },
    capacityPayments : {
      commitmentAmount : {value : 30 , selectedMeasureUnit : "%"},
      commitmentPayment : {value : 30 , selectedMeasureUnit : "kW"},
    }
  });
  React.useEffect(()=>
  {
    setState({...state , initialInvestment : {...state.initialInvestment , bessCost : bessCost , totalInitialInvestment : bessCost + 1300}});
  } , [bessCost])
  const [formHelpers, setFormHelpers] = React.useState(
    {
      projectDebt : {
        label: "Project Debt",
        accessor: "projectDebt",
        fields: [
          {
            label: "DEBT Amount",
            accessor: "debtAmount",
            multipleMeasureUnits: ["%", "$"],
          },
          { label: "Loan Term", accessor: "loanTerm" },
          { label: "Loan Rate", accessor: "loanRate" },
        ],
      },
      initialInvestment : {
        label : "Total Initial Investment",
        accessor : "initialInvestment",
        fields : [
          {
            label : "project length",
            accessor : "project_length",
            multipleMeasureUnits : ["days" , "years"],
          },
          {
            label : "BESS Cost",
            accessor : "bessCost",
            readOnly : true,
          },
          {
            label : "Differential",
            accessor : "differential",
            multipleMeasureUnits : ["%" , "$"],
          },
          {
            label : "Total",
            accessor : "totalInitialInvestment",
            readOnly : true,
          }
        ]
      },
      reserveAccounts : {
        label : "Reserve Accounts",
        accessor : "reserveAccounts",
        fields : [
          {
            label : "Reserve Amount",
            accessor : "reserveAmount",
            multipleMeasureUnits : ["%" , "$"]
          },
          {
            label : "Interest Rate",
            accessor : "interestRate"
          }
        ]
      },
      utilityBill : {
        label : "Utility Bill",
        accessor : "utilityBill",
        fields : [
          {
            label : "Average Demand Rate",
            accessor : "averageDemandRate"
          },
          {
            label : "Average Energy Rate",
            accessor : "averageEnergyRate"
          },
          {
            label : "Monthly Fixed Amount",
            accessor : "monthlyFixedAmount"
          }
        ]},
        investmentTaxCredit : {
          label : "Investment Tax Credit",
          accessor : "investmentTaxCredit",
          fields : [
            {
              label : "Fedral",
              accessor : "fedral",
              multipleMeasureUnits : ["%" , "$"]
            },
          ]
        },
        taxes : {
          label : "Taxes",
          accessor : "taxes",
          fields : [
            {
              label : "Fedral Income Tax",
              accessor : "fedralIncomeTax"
            },
            {
              label : "State Income Tax",
              accessor : "stateIncomeTax"
            },
            {
              label : "Insurance Rate",
              accessor : "insuranceRate"
            },
            {
              label : "Sales Tax",
              accessor : "salesTax"
            },
            {
              label : "Property Tax",
              accessor : "propertyTax"
            },
            {
              label : "Assessed Value",
              accessor : "AssedssedValue"
            },
            {
              label : "Assessed Percent",
              accessor : "AssedssedPercent"
            }
          ]
        },
        capacityPayments : {
          label : "Capacity Payments",
          accessor : "capacityPayments",
          fields : [
            {
              label : "Commitment Amount",
              accessor : "commitmentAmount",
              multipleMeasureUnits : ["%" , "kW"]
            },
            {
              label : "Commitment Payment",
              accessor : "commitmentPayment",
              multipleMeasureUnits : ["kW" , "$"]
            }
          ]
        }
    },

  );
  const [selectedParameters , setSelectedParameters] = React.useState([]);
  const parameters =[
    {label : "Total Initial Investment" , accessor : "initialInvestment"},
    {label : "Project Debt" , accessor : "projectDebt"},
    {label : "Reserve Accounts" , accessor : "reserveAccounts"}
    ,{label : "Utility Bill" , accessor : "utilityBill"},
    {label : "Investment Tax Credit" , accessor : "investmentTaxCredit"},
    {label : "Taxes" , accessor : "taxes"},
    {label : "Capacity Payments" , accessor : "capacityPayments"}
  ];
  const handleClick = (value)=>
  {
    const existingParameters = new Set(selectedParameters);
    if(existingParameters.has(value))
    {
      existingParameters.delete(value);
    }
    else
    {
      existingParameters.add(value);
    }
    setSelectedParameters([...existingParameters]);
  }
  const handleSubmit = ()=>
  {
   let errors = JSON.parse(JSON.stringify(errorsInitialState));
   let foundError = false;
   selectedParameters.map((val)=>
   {
      const currentState = {...state[val]};
      const fields = formHelpers[val].fields;
      fields.map((feild)=>
      {
        const value = currentState[feild.accessor];
        if(typeof value === "object")
        {
          if(value.value === "")
          {
            foundError = true;
            errors = {...errors , [val] : {...errors[val] , haveError : true , [feild.accessor] : true}}
          }
        }
        else
        {
          if(value === "")
          {
            foundError = true;
            errors = {...errors , [val] : {...errors[val] , haveError : true , [feild.accessor] : true}}
          }
        }
      })
   });
   setErrors(errors);
   if(!foundError)
   {
    const payload = {};
    selectedParameters.map((val)=>
    {
      payload[val] = {...state[val]};
    })
    makeApiRequest({method : "post" , urlPath : "financialAnalysis" , body : payload})
   }
   else
   {
    toast.error("Please fill all the fields");
   }
  }
  return (
    <div className=" w-full h-fit py-[2rem] shrink-0 flex flex-col items-center gap-[4rem] justify-start">
      {!bessCost ? (
        <div className="w-full h-[30rem] flex items-center justify-center">
          <Loader />
        </div>
      ) : (
        <>
          <span className=" w-full text-center text-[2rem] text-slate-400 font-bold pt-[1.5rem]">
            Financial Analysis
          </span>
          <div className=" w-full flex items-center justify-center">
          <div className=" w-[25%] ml-[2rem] shrink-0 flex flex-col items-center">
              <span className=" text-[1.3rem] w-full bg-slate-100 py-[.5rem] text-slate-400 font-semibold">Select Parameters</span>
              {parameters.map((val)=>
              {
                return<button onClick={()=>
                {
                  handleClick(val.accessor);
                }} className={selectedParameters.includes(val.accessor) ? " w-full border-b-[0.05rem] border-blue-900 flex items-center py-[.5rem] px-[1rem] bg-slate-200 justify-between" : " w-full border-b-[0.05rem] border-blue-900 bg-slate-100 flex items-center py-[.5rem] px-[1rem] hover:bg-slate-200 justify-between"}>
                  <span className=" text-[1.2rem] text-slate-700">{val.label}</span>
                  {selectedParameters.includes(val.accessor) ? <span><SVGComponent selector={"tickMark"} width={"w-[1.5rem]"} color="#1E3A8A"/></span> : <></>}
                </button>
              })}  
              <button onClick={()=>
                {
                  handleSubmit();
                }} className=" w-full h-[3rem] flex items-center justify-center shrink-0 mt-[2rem] text-[1.4rem] text-blue-900 border-[0.1rem] border-blue-900 rounded-full">Calculate</button>                       
            </div>
          <Results results={results} renderResultsHelper={renderResultsHelper}/>

          </div>
          <div className=" w-full mt-[4rem] h-fit flex items-start justify-evenly">
            
            {selectedParameters.length > 0 ? <div className=" w-[100%] gap-[2rem] flex flex-wrap  justify-center">
              {formRenderingOrder.map((val , ids)=>
              {
                return selectedParameters.includes(val) ? <RenderForm errors={errors[val]} val={val} key={ids} formHelper={formHelpers[val]} state={state} setState={setState}/> : <></>
              })}
            </div> : <div className=" w-full flex flex-col items-center justify-center">
              <SVGComponent selector="select" width="w-[5rem]" color="#94A3B8"/>
              <span className=" text-[1.5rem] text-slate-400 font-semibold">Please Select a Parameter To Customize</span>
              </div>}
          </div>
        </>
      )}
    </div>
  );
}