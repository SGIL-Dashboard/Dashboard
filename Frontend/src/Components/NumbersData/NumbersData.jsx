import React from "react";
import "./NumbersData.css";
import Loader from "../Loader/Loader";
import axios from "axios";
import toast from "react-hot-toast";
import { patterns } from "../../UTILS/UTILS_PATTERNS";
import { stylings } from "../../UTILS/UTILS_STYLES";
import { globalContext } from "../../Context/Context";
import { useContext, useState } from "react";
import { insertCommas } from "../../UTILS/UTILS_HELPERS";
import ToolTip from "./ToolTip";
export default function NumbersData({
  selectionUpdated,
  setBessCost,
  setBessPower,
}) {
  const { theme } = useContext(globalContext);
  const [inputs, setInputs] = React.useState({
    floatInput1: 967.5,
    floatInput2: 0,
    floatInput3: 24.25,
    floatInput4: 0,
    selectInput: 4,
    depthDischarge: 85,
    footprint: 37,
    bessCapacity: 500,
  });
  const [numberLoaded, setNumberLoaded] = React.useState(false);
  const [underProcess, setUnderProcess] = React.useState(false);
  const [capitalCostSelection, setCapitalCostSelection] = React.useState("kWh");
  const [oAndMCostSelection, setOAndMCostSelection] = React.useState("kWh");
  const [recSelected, setRecSelected] = React.useState(true);
  const [bessCostRec, setBessCostRec] = React.useState(0);
  const [bessOut, setBessOut] = React.useState({});
  const formHelpers = {
    range: [
      {
        label: "BESS Depth of Discharge (%)",
        accessor: "depthDischarge",
        max: 100,
        tooltip:
          "The percentage of a battery energy storage system's (BESS) total capacity that has been discharged, indicating how much of the stored energy has been used. Adjusting the depth of discharge changes the recommended BESS Capacity size.",
      },
      {
        // label: "BESS Footprint (inSUP{2}/ kWh)",
        label: "BESS Footprint (in²/ kWh)",
        accessor: "footprint",
        max: 100,
        tooltip:
          "The amount of space a BESS occupies per unit of energy storage capacity (kWh). A lower footprint indicates a more space-efficient system.",
      },
      {
        label: "BESS Duration",
        accessor: "selectInput",
        max: 4,
        tooltip: `The length of time a BESS can deliver its rated power (kW) based on its total energy capacity (kWh). Changing the battery duration, updates the battery power:
      BESS Power = BESS Capacity/ BESS Duration`,
      },
    ],
    floatInputs: [
      { label: "BESS Capital Cost ($/kWh)", accessor: "floatInput1" },
      { label: "BESS Capital Cost ($/kW)", accessor: "floatInput2" },
      { label: "BESS O&M Cost ($/kWh)", accessor: "floatInput3" },
    ],
  };
  const valuesRenderHelpers = [
    { label: "Est. BESS Capacity (kWh)", accessor: "BESS_capacity" },
    { label: "BESS Power (kW)", accessor: "BESS_power" },
    { label: "BESS Footprint (inSUP{2})", accessor: "BESS_footprint" },
    { label: "BESS Cost", accessor: "BESS_cost" },
  ];
  const handleFetch = async () => {
    try {
      let response = await axios.post(
        "https://api.sgillabs.com/bess_calculation",
        { inputs: { ...inputs, bessCapacity: +inputs.bessCapacity } }
      );
      //  const bess_cost_rec = response.data.BESS_cost;
      setBessCostRec(response.data.BESS_capacity_rec);
      response = await axios.post("https://api.sgillabs.com/bess_calculation", {
        inputs: { ...inputs, bessCapacity: response.data.BESS_capacity_rec },
      });
      setBessOut(response.data);
      setBessCost(response.data.BESS_cost);
      setBessPower(response.data.BESS_power);
      setUnderProcess(false);
      setNumberLoaded(true);
    } catch (error) {
      setUnderProcess(false);
      toast.error("Error fetching  data , please try again later");
    }
  };
  const handleSubmit = async () => {
    try {
      let response = await axios.post(
        "https://api.sgillabs.com/bess_calculation",
        {
          inputs: {
            ...inputs,
            bessCapacity: recSelected ? bessCostRec : +inputs.bessCapacity,
          },
        }
      );
      //  const bess_cost_rec = response.data.BESS_cost;
      setBessOut(response.data);
      setBessCost(response.data.BESS_cost);
      setBessPower(response.data.BESS_power);
      setUnderProcess(false);
      setNumberLoaded(true);
    } catch (error) {
      setUnderProcess(false);
      toast.error("Error fetching  data , please try again later");
    }
  };
  React.useEffect(() => {
    if (selectionUpdated) {
      handleFetch();
    } else {
      setNumberLoaded(false);
    }
  }, [selectionUpdated]);
  return (
    <div className={stylings[theme].calculation.parent}>
      {
        <>
          <form
            className={stylings[theme].calculation.subParent}
            onSubmit={(e) => {
              e.preventDefault();
            }}
          >
            <div className="w-full h-fit justify-between flex">
              <div className="w-1/2 flex flex-col gap-[2rem]">
                {formHelpers.range.map((val, id) => {
                  const words = `${val.label}`.split(
                    patterns.SUPERSCRIPTPATTER
                  );
                  const startingPos = val.label.search(
                    patterns.SUPERSCRIPTPATTER
                  );
                  const value = val.label
                    .slice(startingPos)
                    .split("SUP{")
                    .join("")
                    .split("}")[0];

                  return (
                    <div
                      key={id}
                      className={stylings[theme].calculation.rangeParent}
                    >
                      <label
                        className="text-[1.1rem] relative text-slate-400"
                        htmlFor={`${val.accessor}-${id}`}
                      >
                        {startingPos !== -1
                          ? words.map((val, ids) => {
                              if (ids === 0) {
                                return (
                                  <span>
                                    {val}
                                    <sup>{value}</sup>
                                  </span>
                                );
                              }
                              return <span>{val}</span>;
                            })
                          : val.label}
                        <ToolTip text={val.tooltip} />
                      </label>
                      <div className="w-full flex items-center gap-[.5rem]">
                        <input
                          className={stylings[theme].calculation.rangeInput}
                          onChange={(e) => {
                            setInputs({
                              ...inputs,
                              [val.accessor]: +e.target.value,
                            });
                          }}
                          value={inputs[val.accessor]}
                          type="range"
                          min="0"
                          max={val.max}
                        />
                        <span className="text-[1.1rem]">
                          {inputs[val.accessor]}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
              <div className=" w-[45%] flex flex-col gap-[2rem]">
                <div className="flex items-start justify-start overflow-x-clip flex-col w-full shrink-0">
                  <span className=" text-[1.1rem] relative flex items-center text-slate-400">
                    <label htmlFor="" className=" relative">
                      {"BESS Capital Cost ($/"}
                      <ToolTip
                        text={`The initial expenses associated with purchasing and installing a BESS, including the cost of the batteries themselves, associated hardware, installation, and permitting. BESS Cost = $/kWh * BESS Capacity + $/kW * BESS Power`}
                      />
                    </label>
                    <select
                      value={capitalCostSelection}
                      onChange={(e) => {
                        setCapitalCostSelection(e.target.value);
                      }}
                      className=" outline-none mx-[.3rem] rounded-md border-[0.1rem] border-slate-300 text-center bg-transparent"
                    >
                      <option value={"kWh"}>kWh</option>
                      <option value={"kW"}>kW</option>
                      <option value={"Both"}>kWh & kW</option>
                      {/* <option disabled value={""}>
                    Choose
                  </option> */}
                    </select>

                    {")"}
                  </span>

                  {capitalCostSelection ? (
                    <div
                      style={{
                        transform: `translateX(${
                          capitalCostSelection === "kWh" ||
                          capitalCostSelection === "Both"
                            ? 0
                            : "-50%"
                        })`,
                        gap: capitalCostSelection === "Both" ? "2rem" : 0,
                      }}
                      className="w-[200%] h-[2.7rem] shrink-0 flex duration-300 ease-in-out items-center justify-start"
                    >
                      <input
                        style={{
                          width:
                            capitalCostSelection === "Both" ? "22%" : "50%",
                        }}
                        step="0.01"
                        className={stylings[theme].calculation.floatInput}
                        onChange={(e) => {
                          setInputs({
                            ...inputs,
                            floatInput1: e.target.value,
                          });
                        }}
                        value={inputs.floatInput1}
                        type="number"
                      />
                      <input
                        style={{
                          width:
                            capitalCostSelection === "Both" ? "22%" : "50%",
                        }}
                        step="0.01"
                        className={stylings[theme].calculation.floatInput}
                        onChange={(e) => {
                          setInputs({
                            ...inputs,
                            floatInput2: e.target.value,
                          });
                        }}
                        value={inputs.floatInput2}
                        type="number"
                      />
                    </div>
                  ) : (
                    <div className=" w-full h-[2.7rem] shrink-0"></div>
                  )}
                </div>
                <div className="flex items-start justify-start overflow-x-clip flex-col w-full shrink-0">
                  <span className=" text-[1.1rem] items-center   flex text-slate-400">
                    <label className=" relative">
                      {"BESS O&M Cost ($/"}
                      <ToolTip
                        text={`The ongoing costs associated with operating and maintaining a BESS, including labor, materials, and repairs over its lifetime.
                      BESS O&M Cost = $/kWh * BESS Capacity + $/kW * BESS Power`}
                      />
                    </label>
                    <select
                      value={oAndMCostSelection}
                      onChange={(e) => {
                        setOAndMCostSelection(e.target.value);
                      }}
                      className=" outline-none text-center bg-transparent mx-[.3rem] rounded-md border-[0.1rem] border-slate-300"
                    >
                      <option value={"kWh"}>kWh</option>
                      <option value={"YEAR"}>Year</option>
                      <option value={"Both"}>kWh & Year</option>
                      {/* <option disabled value={""}>
                    Choose
                  </option> */}
                    </select>
                    {")"}
                  </span>

                  {oAndMCostSelection ? (
                    <div
                      style={{
                        transform: `translateX(${
                          oAndMCostSelection === "kWh" ||
                          oAndMCostSelection === "Both"
                            ? 0
                            : "-50%"
                        })`,
                        gap: oAndMCostSelection === "Both" ? "2rem" : 0,
                      }}
                      className="w-[200%] duration-300 ease-in-out shrink-0 flex items-center"
                    >
                      <input
                        style={{
                          width: oAndMCostSelection === "Both" ? "22%" : "50%",
                        }}
                        step="0.01"
                        className={stylings[theme].calculation.floatInput}
                        onChange={(e) => {
                          setInputs({
                            ...inputs,
                            floatInput3: e.target.value,
                          });
                        }}
                        value={inputs.floatInput3}
                        type="number"
                      />
                      <input
                        style={{
                          width: oAndMCostSelection === "Both" ? "22%" : "50%",
                        }}
                        step="0.01"
                        className={stylings[theme].calculation.floatInput}
                        onChange={(e) => {
                          setInputs({
                            ...inputs,
                            floatInput4: e.target.value,
                          });
                        }}
                        value={inputs.floatInput4}
                        type="number"
                      />
                    </div>
                  ) : (
                    <div className=" w-full h-[2.7rem]"></div>
                  )}
                </div>
                <div className="flex items-start justify-start overflow-x-clip flex-col w-full shrink-0">
                  <span className=" text-[1.1rem] items-center   flex text-slate-400">
                    <label className="relative" htmlFor="">
                      {"BESS Capacity ("}
                      <ToolTip
                        text={`The total amount of energy, typically measured in kilowatt-hours (kWh), that a BESS can store or deliver.
                        The recommended BESS Capacity is based on the load profile to determine the smallest battery needed to shave peak demand the highest daily demand average for the year.
                        `}
                      />
                    </label>
                    <select
                      value={recSelected}
                      onChange={(e) => {
                        setRecSelected(e.target.value === "true");
                      }}
                      className=" outline-none text-center bg-transparent mx-[.3rem] rounded-md border-[0.1rem] border-slate-300"
                    >
                      <option value={true}>Recommended</option>
                      <option value={false}>Custom</option>
                    </select>
                    {")"}
                  </span>

                  {/* {oAndMCostSelection ?  : <div className=" w-full h-[2.7rem]"></div>} */}
                  <div
                    style={{
                      transform: `translateX(${!recSelected ? 0 : "-50%"})`,
                      gap: oAndMCostSelection === 0,
                    }}
                    className="w-[200%] duration-300 ease-in-out shrink-0 flex items-center"
                  >
                    <input
                      style={{ width: "50%" }}
                      step="0.01"
                      className={stylings[theme].calculation.floatInput}
                      onChange={(e) => {
                        setInputs({
                          ...inputs,
                          bessCapacity: e.target.value,
                        });
                      }}
                      value={inputs.bessCapacity}
                      type="number"
                    />
                    <span
                      style={{ width: "50%" }}
                      className={`${stylings[theme].calculation.floatInput} text-start font-bold text-blue-900`}
                    >
                      {bessCostRec}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div className=" w-full flex mt-[2rem] py-[.5rem] items-center justify-start">
              <button
                onClick={() => {
                  setUnderProcess(true);
                  if (!underProcess) {
                    handleSubmit();
                  }
                }}
                className={stylings[theme].calculation.submitButton}
              >
                {underProcess ? (
                  <div className=" w-[2rem] h-[2rem] border-[0.15rem] border-blue-900 rounded-full shrink-0 animate-spin border-y-white"></div>
                ) : (
                  "Submit"
                )}
              </button>
            </div>
          </form>
          <div className="div w-[40%] px-[1rem] h-full flex items-center justify-center">
            {numberLoaded ? (
              <>
                <div className=" w-full flex flex-wrap justify-between gap-y-[4rem]">
                  {valuesRenderHelpers.map((val, id) => {
                    const afterPoint = `${bessOut[val.accessor]}`.split(".")[1];
                    const words = `${val.label}`.split(
                      patterns.SUPERSCRIPTPATTER
                    );
                    const startingPos = val.label.search(
                      patterns.SUPERSCRIPTPATTER
                    );
                    const value = val.label
                      .slice(startingPos)
                      .split("SUP{")
                      .join("")
                      .split("}")[0];
                   
                    return (
                      <div
                        key={id}
                        className=" w-[40%] justify-center flex flex-col items-center"
                      >
                        <div className="div flex flex-col">
                          <label className=" whitespace-nowrap text-[1rem] text-slate-400">
                            {startingPos !== -1
                              ? words.map((val, ids) => {
                                  if (ids === 0) {
                                    return (
                                      <span>
                                        {val}
                                        <sup>{value}</sup>
                                      </span>
                                    );
                                  }
                                  return <span>{val}</span>;
                                })
                              : val.label}
                          </label>
                          <span className={stylings[theme].calculation.value}>
                            {val.accessor === "BESS_cost"
                              ? `${"$"}${insertCommas(
                                  `${bessOut[val.accessor]}`.split(".")[0]
                                )}${afterPoint ? `.${afterPoint}` : ""}`
                              : bessOut[val.accessor]}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </>
            ) : (
              <>
                <div className=" w-full h-[18rem] flex items-center justify-center">
                  <Loader />
                </div>
              </>
            )}
          </div>
        </>
      }
    </div>
  );
}
