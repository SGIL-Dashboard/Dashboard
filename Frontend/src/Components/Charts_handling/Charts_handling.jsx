import React from "react";
import SVGComponent from "../SVGS/SVGS";
import axios from "axios";
import Plot from "react-plotly.js";
import Plotly from "plotly.js/lib/core";
import createPlotlyComponent from "react-plotly.js/factory";
import Loader from "../Loader/Loader";
import { stylings } from "../../UTILS/UTILS_STYLES";
import { globalContext } from "../../Context/Context";
import { useContext } from "react";
import TimeTaker from "./timeTaker";
import toast from "react-hot-toast";
import ToolTip from "../NumbersData/ToolTip";
const PlotlyComponent = createPlotlyComponent(Plotly);

export default function Charts_handling({ selectionUpdated, selectedOption }) {
  const selectedBuilding = selectedOption.split(".xlsx")[0];
  const { theme } = useContext(globalContext);
  const [selected, setSelected] = React.useState(0);
  const [loaded, setLoaded] = React.useState(false);

  const charts = [
    { title: `Monthly Load Profile: ${selectedBuilding}`, toolTip : "Load Profile" },
    { title: `Date Range Load Profile: ${selectedBuilding}`, toolTip : "Date Range Load Profile" },
    { title: `Monthly Peak and Average Demand: ${selectedBuilding}`, toolTip : "Monthly Peak and Average Demand" },
    { title: `Load Profile for ${selectedBuilding}: Monthly Variation`, toolTip : "Load Profile for Monthly Variation" },
    { title: `Load Profile for ${selectedBuilding}: Daily Variation`, toolTip : "Load Profile for Daily Variation" },
    { title: `Forecasted Load Profile for ${selectedBuilding}`, toolTip : "Forecasted Load Profile" },
    // `Monthly Load Profile: ${selectedBuilding}`,
    // `Date Range Load Profile: ${selectedBuilding}`,
    // `Monthly Peak and Average Demand: ${selectedBuilding}`,
    // `Load Profile for ${selectedBuilding}: Monthly Variation`,
    // `Load Profile for ${selectedBuilding}: Daily Variation`,
    // `Forecasted Load Profile for ${selectedBuilding}`,
  ];
  const [month3Data, setMonth3Data] = React.useState({});
  const [profileData, setProfileData] = React.useState({});
  const [daily3Data, setDaily3Data] = React.useState({});
  const [dateRangeProfileData, setDateRangeProfileData] = React.useState({});
  const [plotData, setPlotData] = React.useState({});
  const [selectedMonth, setSelectedMonth] = React.useState(1);
  const [checkboxes, setCheckboxes] = React.useState({
    option1: false,
    option2: false,
    option3: false,
    // Add more options as needed
  });
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const [timeSelection, setTimeSelection] = React.useState({
    from: "2019-01-01T00:00",
    to: "2019-01-01T23:59",
  });

  const BarGraphlayout = {
    title: charts[1].title,
    xaxis: { title: "Month" },
    yaxis: { title: "Demand" },
    barmode: "stack", // Use 'group' for grouped bars
    height: "600",
  };
  const covertData = (response) => {
    const PeakDaily = Object.values(response?.PeakDailyDemand);
    const MonthlyPeak = Object.values(response?.MonthlyPeakDemand);
    const MaxDemandShaving = Object.values(response?.MaxDemandShaving);

    const data = [
      {
        x: response?.Month,
        y: PeakDaily,
        type: "bar",
        name: "PeakDailyDemand",
        marker: { color: "blue" },
        hoverinfo: MonthlyPeak,
        hovertext: response?.MonthlyPeakDemand.map(
          (demand) => `Monthly Peak Demand: ${demand}`
        ),
      },
      {
        x: response?.Month,
        y: MaxDemandShaving,
        type: "bar",
        name: "MaxDemandShaving",
        marker: { color: "orange" },
        hoverinfo: MonthlyPeak,
        hovertext: response?.MonthlyPeakDemand.map(
          (demand) => `Monthly Peak Demand: ${demand}`
        ),
      },
    ];
    console.log("our bar graph data", data);
    return data;
  };

  const handleFetchData = async () => {
    try {
      const month3Data = await axios.get(
        "https://api.sgillabs.com/give_comp_3D_monthly_plot"
      );
      setMonth3Data(JSON.parse(month3Data.data));
      const daily3Data = await axios.get(
        "https://api.sgillabs.com/give_comp_3D_daily_plot"
      );
      setDaily3Data(JSON.parse(daily3Data.data));
      const profileData = await axios.post(
        "https://api.sgillabs.com/monthly_demand_profile",
        { selectedMonth, checkboxes }
      );
      setProfileData(JSON.parse(profileData.data));
      const dateRangeProfileData = await axios.post(
        "https://api.sgillabs.com/date_filter",
        {timeSelection}
      );

      // const dateRangeProfileData = await axios.post(
      //   "https://api.sgillabs.com/monthly_demand_profile",
      //   { selectedMonth, checkboxes }
      // );
      setDateRangeProfileData(JSON.parse(dateRangeProfileData.data));
      const plotData = await axios.get(
        "https://api.sgillabs.com/get_demand_plot_data"
      );
      setPlotData(covertData(plotData.data));
      setLoaded(true);
    } catch (error) {
      console.error("Error fetching  data:", error);
    }
  };
  React.useEffect(() => {
    if (selectionUpdated) {
      console.log("this is selection oneone", { selectionUpdated });
      handleFetchData();
    } else {
      setLoaded(false);
    }
  }, [selectionUpdated]);
  const handleUpdate = async () => {
    const profileData = await axios.post(
      "https://api.sgillabs.com/monthly_demand_profile",
      { selectedMonth, checkboxes }
    );
    setProfileData(JSON.parse(profileData.data));
  };
  const handleUpdateDateRangeProfileData = async () => {
    const dateRangeProfileData = await axios.post(
      "https://api.sgillabs.com/date_filter",
      { timeSelection}
    );
    // const dateRangeProfileData = await axios.post(
    //   "https://api.sgillabs.com/monthly_demand_profile",
    //   { selectedMonth , checkboxes}
    // );
    setDateRangeProfileData(JSON.parse(dateRangeProfileData.data));
};
  React.useEffect(() => {
    handleUpdate();
  }, [selectedMonth, checkboxes]
  );
  React.useEffect(() => {
    if (new Date(timeSelection.from) < new Date(timeSelection.to)) {
      handleUpdateDateRangeProfileData();
    } else {
      toast.error("From Date should be less than To Date");
    }
  }, [timeSelection]);
  const formHelpers = [
    { label: "Peak Daily Avg. Demand", accessor: "option1" },
    { label: "Monthly Avg. Demand", accessor: "option2" },
    { label: "Peak Demand", accessor: "option3" },
  ];
  const darkThemeChartStylings =
    theme === "dark"
      ? {
          paper_bgcolor: "#1F2937",
          font: { color: "#94A3B8" },
          plot_bgcolor: "#1F2937",
        }
      : {};
  const chartsParentStylings =
    "relative w-full h-[41rem] shrink-0 flex flex-col items-center justify-center";
  return (
    <div className={stylings[theme].chartSelection.parent}>
      <div
        className={stylings[theme].chartSelection.chartSelectorContainer.parent}
      >
        <span className=" text-[1.3rem] font-semibold text-slate-400">
          Chart Selection
        </span>
        <div className="w-full flex flex-col items-center">
          {charts.map((val, id) => {
            return (
              <button
                onClick={() => {
                  setSelected(id);
                }}
                key={id}
                className={
                  selected === id
                    ? stylings[theme].chartSelection.chartSelectorContainer
                        .button.selected
                    : stylings[theme].chartSelection.chartSelectorContainer
                        .button.notSelected
                }
              >
                <label
                  className={
                    `${stylings[theme].chartSelection.chartSelectorContainer.span} relative`
                  }
                >
                  <ToolTip left={true} text={val.toolTip}/>
                  {val.title}
                </label>
              </button>
            );
          })}
        </div>
      </div>
      <div className="w-[70%] flex flex-col h-[41rem] justify-start shrink-0 overflow-hidden items-center">
        {loaded ? (
          <div
            style={{ transform: `translateY(${-selected * 41}rem)` }}
            className=" w-full ease-in-out duration-500 h-[600%] shrink-0 flex flex-col items-center"
          >
            <div className={`MonthlyChart ${chartsParentStylings}`}>
              <div className="w-full h-full flex flex-col items-center justify-center gap-[1rem]">
                <SVGComponent selector="clock" width="w-[4rem]" color="grey"/>
                <span className="text-[1.4rem] text-slate-500 font-semibold">
                  Getting Your Chart Ready Please Wait
                </span>
              </div>
              {profileData?.data && (
                <div className=" w-full pt-[1rem] h-full absolute top-0 left-0 flex flex-col items-center justify-start z-[1]">
                  <PlotlyComponent
                    data={profileData.data}
                    layout={{
                      ...profileData.layout,
                      height: 500,
                      width: 790,
                      ...darkThemeChartStylings,
                    }}
                  />
                  <div className=" flex-grow flex items-center justify-evenly w-full">
                    <select
                      className={
                        stylings[theme].chartSelection.chartSelectorContainer
                          .form.select
                      }
                      onChange={(e) => {
                        setSelectedMonth(e.target.value);
                      }}
                      value={selectedMonth}
                    >
                      {months.map((val, id) => {
                        return (
                          <option key={id} value={id + 1}>
                            {val}
                          </option>
                        );
                      })}
                    </select>
                      {formHelpers.map((val, id) => {
                        return (
                          <div
                            key={id}
                            className=" flex items-center gap-[.5rem]"
                          >
                            <input
                              checked={checkboxes[val.accessor]}
                              onChange={(e) => {
                                setCheckboxes({
                                  ...checkboxes,
                                  [val.accessor]: e.target.checked,
                                });
                              }}
                              id={val.accessor}
                              type="checkbox"
                              className=" w-[1.3rem] h-[1.3rem]"
                            />
                            <label
                              className={
                                stylings[theme].chartSelection
                                  .chartSelectorContainer.form.label
                              }
                              htmlFor={val.accessor}
                            >
                              {val.label}
                            </label>
                          </div>
                        );
                      })}

                    {/* {formHelpers.map((val , id)=>
              {
                return<div key={id} className=" flex items-center gap-[.5rem]"><input checked={checkboxes[val.accessor]} onChange={(e)=>
                {
                  setCheckboxes({...checkboxes , [val.accessor]:e.target.checked})
                }} id={val.accessor} type="checkbox" className=' w-[1.3rem] h-[1.3rem]'/>
                <label className={stylings[theme].chartSelection.chartSelectorContainer.form.label} htmlFor={val.accessor}>{val.label}</label>
                </div>
              })} */}
                  </div>
                </div>
              )}
            </div>
            <div className={`MonthlyChart ${chartsParentStylings}`}>
              <div className="w-full h-full flex flex-col items-center justify-center gap-[1rem]">
                <SVGComponent selector="clock" width="w-[4rem]" color="grey" />
                <span className="text-[1.4rem] text-slate-500 font-semibold">
                  Getting Your Chart Ready Please Wait
                </span>
              </div>
              {dateRangeProfileData?.data && (
                <div className=" w-full pt-[1rem] h-full absolute top-0 left-0 flex flex-col items-center justify-start z-[1]">
                  <PlotlyComponent
                    data={dateRangeProfileData.data}
                    layout={{
                      ...dateRangeProfileData.layout,
                      height: 500,
                      width: 790,
                      ...darkThemeChartStylings,
                    }}
                  />
                  <div className=" flex-grow flex items-center justify-center gap-[2rem] w-full">
                    <TimeTaker
                      label={"From"}
                      current="from"
                      comparision="to"
                      lessThan={true}
                      timeSelection={timeSelection}
                      setTimeSelection={setTimeSelection}
                    />
                    <TimeTaker
                      label={"To"}
                      current="to"
                      comparision="from"
                      lessThan={false}
                      timeSelection={timeSelection}
                      setTimeSelection={setTimeSelection}
                    />
                    {/* <div className="div px-[.5rem] relative w-[17rem] h-[6.3rem] rounded-xl justify-center shrink-0 flex flex-col border-[0.15rem] border-slate-400">
                <span className=' text-[1.1rem] bg-white items-center absolute px-[.5rem] top-[-0.9rem] left-[1rem]  flex text-slate-400 '>Markings</span>
                {formHelpers.map((val , id)=>
              {
                return<div key={id} className=" flex items-center gap-[.5rem]"><input checked={checkboxes[val.accessor]} onChange={(e)=>
                {
                  setCheckboxes({...checkboxes , [val.accessor]:e.target.checked})
                }} id={val.accessor} type="checkbox" className=' w-[1.3rem] h-[1.3rem]'/>
                <label className={stylings[theme].chartSelection.chartSelectorContainer.form.label} htmlFor={val.accessor}>{val.label}</label>
                </div>
              })}
              </div> */}
                    {/* <div className="div px-[.5rem] relative w-[17rem] h-[6.3rem] rounded-xl justify-center shrink-0 flex flex-col border-[0.15rem] border-slate-400">
                <span className=' text-[1.1rem] bg-white items-center absolute px-[.5rem] top-[-0.9rem] left-[1rem]  flex text-slate-400 '>Markings</span>
                {formHelpers.map((val , id)=>
              {
                return<div key={id} className=" flex items-center gap-[.5rem]"><input checked={checkboxes[val.accessor]} onChange={(e)=>
                {
                  setCheckboxes({...checkboxes , [val.accessor]:e.target.checked})
                }} id={val.accessor} type="checkbox" className=' w-[1.3rem] h-[1.3rem]'/>
                <label className={stylings[theme].chartSelection.chartSelectorContainer.form.label} htmlFor={val.accessor}>{val.label}</label>
                </div>
              })}
              </div> */}
                    {/* {formHelpers.map((val , id)=>
              {
                return<div key={id} className=" flex items-center gap-[.5rem]"><input checked={checkboxes[val.accessor]} onChange={(e)=>
                {
                  setCheckboxes({...checkboxes , [val.accessor]:e.target.checked})
                }} id={val.accessor} type="checkbox" className=' w-[1.3rem] h-[1.3rem]'/>
                <label className={stylings[theme].chartSelection.chartSelectorContainer.form.label} htmlFor={val.accessor}>{val.label}</label>
                </div>
              })} */}
                  </div>
                </div>
              )}
            </div>
            <div className={` MonthlyChart pt-[3rem] ${chartsParentStylings}`}>
              <div className="w-full h-full flex flex-col items-center justify-center gap-[1rem]">
                <SVGComponent selector="clock" width="w-[4rem]" color="grey" />
                <span className="text-[1.4rem] text-slate-500 font-semibold">
                  Getting Your Chart Ready Please Wait
                </span>
              </div>
              {plotData && (
                <div className=" w-full translate-y-[-20px] h-full absolute top-0 left-0 flex flex-col items-center justify-center z-[1]">
                  <Plot
                    data={plotData}
                    layout={{
                      ...BarGraphlayout,
                      height: 600,
                      width: 790,
                      ...darkThemeChartStylings,
                    }}
                  />
                </div>
              )}
            </div>
            <div className={`${chartsParentStylings}`}>
              <div className="w-full h-full flex flex-col items-center justify-center gap-[1rem]">
                <SVGComponent selector="clock" width="w-[4rem]" color="grey" />
                <span className="text-[1.4rem] text-slate-500 font-semibold">
                  Getting Your Chart Ready Please Wait
                </span>
              </div>
              {daily3Data?.data && (
                <div className=" w-full  translate-y-[-20px] h-full absolute top-0 left-0 flex flex-col items-center justify-center z-[1]">
                  <Plot
                    data={month3Data.data}
                    layout={{
                      ...month3Data.layout,
                      height: 600,
                      width: 790,
                      template: {
                        ...month3Data.layout.template,
                        layout: {
                          ...month3Data.layout.template.layout,
                          ...darkThemeChartStylings,
                        },
                      },
                    }}
                  />
                </div>
              )}
            </div>
            <div className={`${chartsParentStylings}`}>
              <div className="w-full h-full flex flex-col items-center justify-center gap-[1rem]">
                <SVGComponent selector="clock" width="w-[4rem]" color="grey" />
                <span className="text-[1.4rem] text-slate-500 font-semibold">
                  Getting Your Chart Ready Please Wait
                </span>
              </div>
              {daily3Data?.data && (
                <div className=" w-full  translate-y-[-20px] h-full absolute top-0 left-0 flex flex-col items-center justify-center z-[1]">
                  <Plot
                    data={daily3Data.data}
                    layout={{
                      ...daily3Data.layout,
                      height: 600,
                      width: 790,
                      template: {
                        ...daily3Data.layout.template,
                        layout: {
                          ...daily3Data.layout.template.layout,
                          ...darkThemeChartStylings,
                        },
                      },
                    }}
                  />
                </div>
              )}
            </div>
            <div className={`MonthlyChart ${chartsParentStylings}`}>
              <div className="w-full h-full flex flex-col items-center justify-center gap-[1rem]">
                <SVGComponent selector="clock" width="w-[4rem]" color="grey" />
                <span className="text-[1.4rem] text-slate-500 font-semibold">
                  Getting Your Chart Ready Please Wait
                </span>
              </div>
              {dateRangeProfileData?.data && (
                <div className=" w-full pt-[1rem] h-full absolute top-0 left-0 flex flex-col items-center justify-start z-[1]">
                  <PlotlyComponent
                    data={profileData.data}
                    layout={{
                      ...profileData.layout,
                      height: 500,
                      width: 790,
                      title : {text : `Forecasted Load Profile For ${selectedBuilding}`},
                      ...darkThemeChartStylings,
                    }}
                  />
                  <div className=" flex-grow flex h-fit items-center justify-center w-full">
                    <div className=" flex w-full justify-center gap-[2rem]">
                    <TimeTaker
                      label={"From"}
                      current="from"
                      comparision="to"
                      lessThan={true}
                      timeSelection={timeSelection}
                      setTimeSelection={setTimeSelection}
                    />
                    <TimeTaker
                      label={"To"}
                      current="to"
                      comparision="from"
                      lessThan={false}
                      timeSelection={timeSelection}
                      setTimeSelection={setTimeSelection}
                    />
                    <div className="div relative w-[25%] py-[1rem] rounded-xl justify-center shrink-0 flex flex-col border-[0.15rem] items-center border-slate-400">
                    <span className={stylings[theme].chartSelection.chartSelectorContainer.timeTakers.heading}>Markings</span>
                    <div className=" flex flex-col items-start">
                    {formHelpers.map((val, id) => {
                        return (
                          <div
                            key={id}
                            className=" flex items-center gap-[.5rem]"
                          >
                            <input
                              checked={checkboxes[val.accessor]}
                              onChange={(e) => {
                                setCheckboxes({
                                  ...checkboxes,
                                  [val.accessor]: e.target.checked,
                                });
                              }}
                              id={val.accessor}
                              type="checkbox"
                              className=" w-[1.3rem] h-[1.3rem]"
                            />
                            <label
                              className={
                                stylings[theme].chartSelection
                                  .chartSelectorContainer.form.label
                              }
                              htmlFor={val.accessor}
                            >
                              {val.label}
                            </label>
                          </div>
                        );
                      })}
                    </div>
                    </div>
                    </div>
                    
                    
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className=" w-full h-full flex flex-col items-center justify-center">
            <Loader />
          </div>
        )}
      </div>
    </div>
  );
}
