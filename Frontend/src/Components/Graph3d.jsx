import React, { useEffect, useState } from "react";
import axios from "axios";
import createPlotlyComponent from "react-plotly.js/factory";
import Plotly from "plotly.js/lib/core";
import Plot from "react-plotly.js";
import "./Graph3d.css";
const PlotlyComponent = createPlotlyComponent(Plotly);

const Graph3d = () => {
  const [month3Data, setMonth3Data] = useState({});
  const [daily3Data, setDaily3Data] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch3dMonthlyData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/give_comp_3D_monthly_plot"
        );
        // console.log("data=>", response.data);
        const month_data = JSON.parse(response.data);
        setMonth3Data(month_data);
      } catch (error) {
        console.error("Error fetching plot data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetch3dMonthlyData();

    const fetch3dDailyData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/give_comp_3D_daily_plot"
        );
        // console.log("data=>", response.data);
        const daily_data = JSON.parse(response.data);
        setDaily3Data(daily_data);
      } catch (error) {
        console.error("Error fetching plot data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetch3dDailyData();
  }, []);

  if (loading) {
    return (
      <div>
        <h2
          style={{
            color: "green",
            fontSize: "60px",
            marginLeft: "20px",
            marginRight: "20px",
          }}
        >
          Loading....
        </h2>
      </div>
    );
  } else {
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          margin: "auto",
        }}
      >
        <div>
          {month3Data?.data ? (
            <Plot data={month3Data.data} layout={month3Data.layout} />
          ) : (
            ""
          )}
        </div>
        <div style={{ marginLeft: "5%" }}>
          {daily3Data?.data ? (
            <Plot data={daily3Data.data} layout={daily3Data.layout} />
          ) : (
            ""
          )}
        </div>
      </div>
    );
  }
};
export default Graph3d;
