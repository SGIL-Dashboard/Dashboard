import React from "react";
import { stylings } from "../../UTILS/UTILS_STYLES";
import { globalContext } from "../../Context/Context";
import {insertCommas} from "../../UTILS/UTILS_HELPERS";
export default function RenderForm({ formHelper, state, setState, errors  , val , bessPower}) {
  console.log({ formHelper, errors });
  const { theme } = React.useContext(globalContext);
  const fieldsLen = formHelper?.fields?.length;
  const parentStylings = errors?.haveError
    ? fieldsLen > 4
      ? "w-[30%] flex mt-[1rem] justify-between flex-wrap p-[1rem] py-[1.5rem] border-[0.15rem] border-red-500 rounded-lg relative items-center"
      : "w-[30%] flex mt-[1rem] flex-col p-[1rem] py-[1.5rem] border-[0.15rem] border-red-500 rounded-lg relative items-center justify-evenly"
    : fieldsLen > 4
    ? "w-[30%] flex mt-[1rem]  justify-between flex-wrap p-[1rem] py-[1.5rem] border-[0.15rem] border-slate-400 rounded-lg relative items-center"
    : "w-[30%] flex mt-[1rem] flex-col p-[1rem] py-[1.5rem] border-[0.15rem] border-slate-400 rounded-lg relative items-center justify-evenly";
  return <>
  {val === "demandResponse" ? <form className=" w-[30%] mt-[1rem] p-[1rem] border-[0.15rem] rounded-lg relative flex flex-col items-center justify-center">
  <div className=" w-full justify-between flex pt-[1rem] items-center">
        <span className=" absolute top-[-1rem] bg-white text-slate-400 text=[1.1rem] left-[1rem] px-[.5rem]">Demand Response</span>
        <span className=" flex-1 text-start text-slate-400  text-[0.9rem]">Months</span>
        <span className=" flex-1 text-[0.9rem] text-slate-400 flex flex-col "><span>Commitment</span> <span>Amount {"("}<select className=" text-center outline-none" onChange={(e)=>
          {
            const demandResponse = state.demandResponse.inputs;
            const value = e.target.value;
            if(value === "%")
            {
              Object.keys(demandResponse).map((val)=>
              {
                const commitmentPayment = demandResponse[val].CommitmentPayment;
                const commitmentAmount = demandResponse[val].CommitmentAmount;
                const total = ((commitmentAmount / 100) * bessPower) * commitmentPayment;
                demandResponse[val].totalDrPayment = total;
              })
            }
            else
            {
              Object.keys(demandResponse).map((val)=>
              {
                const commitmentPayment = demandResponse[val].CommitmentPayment;
                const commitmentAmount = demandResponse[val].CommitmentAmount;
                const total = commitmentAmount * commitmentPayment;
                demandResponse[val].totalDrPayment = total;
              })
            }
            setState({
              ...state,
              demandResponse: {
                inputs : {...demandResponse},
                selectedCommetmentAmount: e.target.value,
              },
            })
          }} value={state.demandResponse.selectedCommetmentAmount}>
          <option value="kW">kW</option>
          <option value="%">%</option>
          </select>{")"}</span></span>
        <span className=" flex-1 text-[0.9rem] text-slate-400">Commitment Payment</span>
        <span className=" flex-1 text-[0.9rem] text-slate-400">Total DR Payment ($)</span>
      </div>
    {formHelper.fields.map((val) => 
    {
      return <div className=" w-full justify-between flex items-center">
        <span className=" absolute top-[-1rem] bg-white text-slate-400 text=[1.1rem] left-[1rem] px-[.5rem]">Demand Response</span>
        <span className=" flex-1 font-semibold text-start text-blue-900 text-[1.2rem]">{val.label}</span>
        <input type="text" className=" ULInput w-[25%] shrink-0 text-center outline-none" onChange={(e)=>
          {
            const value = +e.target.value;
            if(`${value}` === "NaN")
            {
              return
            }

            const commitmentPayment = state[formHelper.accessor].inputs[val.accessor].CommitmentPayment;
            const selection = state.demandResponse.selectedCommetmentAmount;
            let total = 0;
            if(selection === "%")
            {
              total =  ((value / 100) * bessPower) * commitmentPayment;
            }
            else
            {
              total = (value * commitmentPayment);
            }
            
            setState({
              ...state,
              [formHelper.accessor]: {
                ...state[formHelper.accessor],
                inputs: {
                  ...state[formHelper.accessor].inputs,
                  [val.accessor]: {
                    ...state[formHelper.accessor].inputs[val.accessor],
                    CommitmentAmount : +e.target.value,
                    totalDrPayment : total
                  }
                }
              }
            })
          }} value={state[formHelper.accessor].inputs[val.accessor].CommitmentAmount}/>
        <input type="text" className=" ULInput w-[25%] shrink-0 text-center outline-none" onChange={(e)=>
          {
            const value = +e.target.value;
            if(`${value}` === "NaN") return
            const commitmentAmount = +state[formHelper.accessor].inputs[val.accessor].CommitmentAmount;
            const selection = state.demandResponse.selectedCommetmentAmount;
            let total = 0;
            if(selection === "%")
            {
              total =  ((commitmentAmount / 100) * bessPower) * value;
            }
            else
            {
              total = (commitmentAmount * value);
            }

            setState({
              ...state,
              [formHelper.accessor]: {
                ...state[formHelper.accessor],
                inputs: {
                  ...state[formHelper.accessor].inputs,
                  [val.accessor]: {
                    ...state[formHelper.accessor].inputs[val.accessor],
                    CommitmentPayment : +e.target.value,
                    totalDrPayment : +total
                  }
                }
              }
            })
          }} value={state[formHelper.accessor].inputs[val.accessor].CommitmentPayment}/>
       <span className="flex-1">{state[formHelper.accessor].inputs[val.accessor].totalDrPayment}</span>
        {/* <span className=" flex-1">{state[formHelper.accessor].inputs[val.accessor].CommitmentPayment}</span> */}
      </div>
    })}
  </form> :<form
      onSubmit={(e) => {
        e.preventDefault();
      }}
      className={parentStylings}
    >
      <span className=" text-[1.3rem] bg-white items-center absolute px-[.5rem] top-[-1.2rem] left-[50%] translate-x-[-50%]  flex text-slate-400">
        {formHelper.label}
      </span>
      {formHelper.fields.map((val) => {
        if (val.multipleMeasureUnits) {
          const selectedVal =
            state[formHelper.accessor][val.accessor].selectedMeasureUnit;
          return (
            <div
              className={
                fieldsLen > 4
                  ? " w-[45%] flex flex-col items-start shrink-0 overflow-hidden"
                  : " w-full flex flex-col items-start shrink-0 overflow-hidden"
              }
            >
              {
                val.type === "span" ? <span>{val.label}</span> : <>
                <label className=" text-[1.1rem] text-slate-400">
                {val.label}
                {"("}
                <select
                  onChange={(e) => {
                    console.log({val})
                    if(formHelper.accessor === "initialInvestment" && val.accessor === "differential")
                    {
                      if(e.target.value === "%")
                      {
                        const bessCost = +state.initialInvestment.bessCost;
                        const percent = +state.initialInvestment.differential.value;
                        const result = bessCost + (percent / 100) * bessCost;
                        setState({
                          ...state,
                          [formHelper.accessor]: {
                            ...state[formHelper.accessor],
                            [val.accessor]: {
                              ...state[formHelper.accessor][val.accessor],
                              selectedMeasureUnit: e.target.value,
                            },
                            totalInitialInvestment : result,
                          },
                        });
                      }
                      else{
                        const bessCost = +state.initialInvestment.bessCost;
                        const dollars  = +state.initialInvestment.differential.value;
                        const result = bessCost + dollars; 
                        setState({
                          ...state,
                          [formHelper.accessor]: {
                            ...state[formHelper.accessor],
                            [val.accessor]: {
                              ...state[formHelper.accessor][val.accessor],
                              selectedMeasureUnit: e.target.value,
                            },
                            totalInitialInvestment : result,
                          },
                        });
                      }
                      return;
                    }
                    setState({
                      ...state,
                      [formHelper.accessor]: {
                        ...state[formHelper.accessor],
                        [val.accessor]: {
                          ...state[formHelper.accessor][val.accessor],
                          selectedMeasureUnit: e.target.value,
                        },
                      },
                    });
                  }}
                  value={selectedVal}
                >
                  <option value={val.multipleMeasureUnits[0]}>
                    {val.multipleMeasureUnits[0]}
                  </option>
                  <option value={val.multipleMeasureUnits[1]}>
                    {val.multipleMeasureUnits[1]}
                  </option>
                </select>
                {")"}
              </label>
              <div
                className=" w-[100%] duration-300 ease-in-out shrink-0 flex items-center justify-start"
              >
                <input
                  onChange={(e) => {
                    if(formHelper.accessor === "initialInvestment" && val.accessor === "differential")
                    {
                      console.log({measureUnit : state[formHelper.accessor][val.accessor].selectedMeasureUnit , val })
                      if(state[formHelper.accessor][val.accessor].selectedMeasureUnit === "%")
                      {
                        const bessCost = state.initialInvestment.bessCost;
                        const percent = +e.target.value;
                        const result = bessCost + (percent / 100) * bessCost;
                        setState({
                          ...state,
                          [formHelper.accessor]: {
                            ...state[formHelper.accessor],
                            [val.accessor]: {
                              ...state[formHelper.accessor][val.accessor],
                              value: +percent,
                            },
                            totalInitialInvestment : result,
                          },
                        });
                      }
                      else{
                        const bessCost = state.initialInvestment.bessCost;
                        const dollars  = +e.target.value;
                        const result = bessCost + dollars; 
                        setState({
                          ...state,
                          [formHelper.accessor]: {
                            ...state[formHelper.accessor],
                            [val.accessor]: {
                              ...state[formHelper.accessor][val.accessor],
                              value: +e.target.value,
                            },
                            totalInitialInvestment : result,
                          },
                        });
                      }
                      return;
                    }
                    else if (val.readOnly) return;
                    setState({
                      ...state,
                      [formHelper.accessor]: {
                        ...state[formHelper.accessor],
                        [val.accessor]: {
                          ...state[formHelper.accessor][val.accessor],
                         value: +e.target.value,
                        },
                      },
                    });
                  }}
                  type="number"
                  style={{ width: "100%" }}
                  className={
                    errors[val.accessor]
                      ? `${stylings[theme].calculation.floatInput} border-red-500`
                      : stylings[theme].calculation.floatInput
                  }
                  value={
                    state[formHelper.accessor][val.accessor].value
                  }
                />
              </div></>
              }
              
            </div>
          );
        }
        return (
          <div
            className={
              fieldsLen > 4
                ? "w-[45%] flex flex-col items-start shrink-0 overflow-hidden"
                : "w-full flex flex-col items-start shrink-0 overflow-hidden"
            }
          >
            <label className=" text-[1.1rem] text-slate-400">{val.label}</label>
            <div className=" w-full flex items-center justify-center"></div>
          {
            val.readOnly ? <span className="text-[1.5rem] font-bold text-blue-900 text-start w-full border-b-[0.15rem] border-blue-900">${insertCommas(state[formHelper.accessor][val.accessor])}</span> : <input
            onChange={(e) => {
              if (val.readOnly) return;
              setState({
                ...state,
                [formHelper.accessor]: {
                  ...state[formHelper.accessor],
                  [val.accessor]: e.target.value,
                },
              });
            }}
            type="number"
            style={{ width: "100%" }}
            className={
              errors[val.accessor]
                ? `${stylings[theme].calculation.floatInput} border-red-500`
                : stylings[theme].calculation.floatInput
            }
            value={state[formHelper.accessor][val.accessor]}
          />
          }
          </div>
        );
      })}
    </form>}
  </>
  ;
}
