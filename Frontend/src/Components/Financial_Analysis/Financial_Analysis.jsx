import React from "react";
import Loader from "../Loader/Loader";
import { stylings } from "../../UTILS/UTILS_STYLES";
import { globalContext } from "../../Context/Context";
import RenderForm from "./RenderForm";
import SVGComponent from "../SVGS/SVGS";
import { makeApiRequest } from "../../UTILS/UTILS_HELPERS";
import toast from "react-hot-toast";
export default function FinancialAnalysis({ bessCost }) {
  const { theme } = React.useContext(globalContext);
  const errorsInitialState = {
    projectDebt : {
      debtAmount : {},
      loanTerm : false,
      loanRate : false
    },
    reserveAccounts : {
      reserveAmount : {},
      interestRate : false
    
    },
    utilityBill : {
      averageDemandRate : false,
      averageEnergyRate : false,
      monthlyFixedAmount : false
    
    },
    initialInvestment : 
    {
      bessCost : false,
      differential : {},
      totalInitialInvestment : false
    },
    investmentTaxCredit : {
      fedral : {},
      state : {}
    
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
      commitmentAmount : {},
      commitmentPayment : {}
    }
 }
  const [errors , setErrors] = React.useState(JSON.parse(JSON.stringify(errorsInitialState)));
  const [state, setState] = React.useState({
    differential: "",
    projectDebt: {
      debtAmount: { "%": 40, $: 50, selectedMeasureUnit: "%" },
      loanTerm: 18,
      loanRate: 5,
    },
    initialInvestment : {
      bessCost : bessCost,
      differential : {"%" : 50 , "$" : "1300" , selectedMeasureUnit : "$"},
      totalInitialInvestment : bessCost + 1300
    },
    reserveAccounts : {
      reserveAmount : {"%" : 10 , "$" : 110 , selectedMeasureUnit : "%"},
      interestRate : 1.5
    },
    utilityBill : {
      averageDemandRate : 20,
      averageEnergyRate : 5,
      monthlyFixedAmount : 200
    },
    investmentTaxCredit : {
      fedral : {
        "%" : 30,
        "$" : 100,
        selectedMeasureUnit : "%"
      },
      state : {
        "%" : 0,
        "$" : 50,
        selectedMeasureUnit : "%"
      }
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
      commitmentAmount : {"%" : 40 , "kW" : 100 , selectedMeasureUnit : "%"},
      commitmentPayment : {"kW" : 40 , "$" : 100 , selectedMeasureUnit : "kW"},
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
            {
              label : "State",
              accessor : "state",
              multipleMeasureUnits : ["%" , "$"]
            }
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
          if(value[value.selectedMeasureUnit] === "")
          {
            foundError = true;
            errors = {...errors , [val] : {...errors[val] , haveError : true , [feild.accessor] : {[value.selectedMeasureUnit] : true}}}
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
          <div className="w-full h-fit shrink-0 flex items-center justify-evenly">
            <div className="flex flex-col items-center">
              <span className="text-[1rem] text-slate-400">BESS COST</span>
              <span className=" text-[2rem] font-bold text-blue-900">
                ${bessCost}
              </span>
            </div>
            <span className="text-[4rem] font-bold text-slate-400">+</span>
            <div className="flex flex-col items-start">
              <label htmlFor="" className="text-[1.1rem] text-slate-400">
                Differential in{" "}
              </label>
              <input
                type="number"
                className="outline-none ULInput bg-transparent  text-[1.5rem] shrink-0 border-b-[0.15rem] duration-300 ease-in-out border-blue-900"
              />
            </div>
            <span className="text-[4rem] font-bold text-slate-400">=</span>
            <div className="flex flex-col items-center">
              <span className="text-[1rem] text-slate-400">
                Total Initial Investment
              </span>
              <span className=" text-[2rem] font-bold text-blue-900">
                ${bessCost}
              </span>
            </div>
          </div>
          <div className=" w-full mt-[4rem] h-fit flex items-start justify-evenly">
            <div className=" w-[25%] shrink-0 flex flex-col items-center">
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
            <div className=" w-[65%] gap-[1rem] flex flex-wrap items-start justify-start">
              {selectedParameters.map((val)=>
              {
                return<RenderForm errors={errors[val]} formHelper={formHelpers[val]} state={state} setState={setState}/>
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
}