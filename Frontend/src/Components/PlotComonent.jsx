import React, { useEffect, useState } from "react";
import axios from "axios";
import createPlotlyComponent from "react-plotly.js/factory";
import Plotly from "plotly.js/lib/core";
import Plot from "react-plotly.js";
// Import necessary Plotly components
// import scatter from "plotly.js/lib/scatter";

// // Register Plotly components
// Plotly.register([scatter]);

const PlotlyComponent = createPlotlyComponent(Plotly);

const PlotComponent = () => {
  // const [monthData, setMonthData] = useState({});
  const [plotData, setPlotData] = useState({});
  const [month3Data, setMonth3Data] = useState({});
  useEffect(() => {
    // const fetch3dDailyData = async () => {
    //   try {
    //     const response = await axios.get(
    //       "http://54.175.34.126:8000/comp_3D_daily_plot"
    //     );
    //     const data = JSON.parse(response.data);
    //     set3DailyData(data);
    //   } catch (error) {
    //     console.error("Error fetching plot data:", error);
    //   }
    // };
    const fetchData = async () => {
      try {
        const response = await axios.get("http://54.175.34.126:8000/get_plot_data");
        const data = JSON.parse(response.data);
        setPlotData(data);
      } catch (error) {
        console.error("Error fetching plot data:", error);
      }
    };
    // const fetchMonthData = async () => {
    //   try {
    //     const response = await axios.get(
    //       "http://54.175.34.126:8000/fig_monthly_Demand_data"
    //     );
    //     const month_data = JSON.parse(response.data);
    //     setMonthData(month_data);
    //   } catch (error) {
    //     console.error("Error fetching plot data:", error);
    //   }
    // };

    const fetch3dMonthlyData = async () => {
      try {
        const response = await axios.get(
          "http://54.175.34.126:8000/give_comp_3D_monthly_plot"
        );
        console.log("data=>", response.data);
        const month_data = JSON.parse(response.data);
        setMonth3Data(month_data);
      } catch (error) {
        console.error("Error fetching plot data:", error);
      }
    };

    fetchData();
    // fetchMonthData();
    // fetch3dDailyData();
    fetch3dMonthlyData();
  }, []);

  // useEffect(() => {
  //   // Check if graphData is available before plotting
  //   if (month3Data) {
  //     // Plot the graph using Plotly.js
  //     Plotly.newPlot("graph-container", month3Data.data, month3Data.layout);
  //   }
  // }, [month3Data]);

  return (
    <div>
      <PlotlyComponent data={plotData.data} layout={plotData.layout} />
      {/* <PlotlyComponent data={daily3Data.data} layout={daily3Data.layout} />  */}
      <Plot data={month3Data.data} layout={month3Data.layout} />
      {/* <div id="graph-container"></div> */}
    </div>
  );
};

export default PlotComponent;
