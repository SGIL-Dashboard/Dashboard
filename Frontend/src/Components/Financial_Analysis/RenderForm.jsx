import React from "react";
import { stylings } from "../../UTILS/UTILS_STYLES";
import { globalContext } from "../../Context/Context";
import {insertCommas} from "../../UTILS/UTILS_HELPERS";
export default function RenderForm({ formHelper, state, setState, errors  , val}) {
  console.log({ formHelper, errors });
  const { theme } = React.useContext(globalContext);
  const fieldsLen = formHelper.fields.length;
  const parentStylings = errors.haveError
    ? fieldsLen > 4
      ? "w-[30%] flex justify-between flex-wrap p-[1rem] py-[1.5rem] border-[0.15rem] border-red-500 rounded-lg relative items-center"
      : "w-[30%] flex flex-col p-[1rem] py-[1.5rem] border-[0.15rem] border-red-500 rounded-lg relative items-center justify-evenly"
    : fieldsLen > 4
    ? "w-[30%] flex  justify-between flex-wrap p-[1rem] py-[1.5rem] border-[0.15rem] border-slate-400 rounded-lg relative items-center"
    : "w-[30%] flex flex-col p-[1rem] py-[1.5rem] border-[0.15rem] border-slate-400 rounded-lg relative items-center justify-evenly";
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
      }}
      className={parentStylings}
    >
      <span className=" text-[1.1rem] bg-white items-center absolute px-[.5rem] top-[-0.9rem] left-[1rem]  flex text-slate-400 ">
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
    </form>
  );
}
