import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";
import Plotly from "plotly.js/lib/core";
import createPlotlyComponent from "react-plotly.js/factory";
const PlotlyComponent = createPlotlyComponent(Plotly);
const DemandFilter = () => {
  const [plotData, setPlotData] = useState(null);
  const [checkboxes, setCheckboxes] = useState({
    option1: false,
    option2: false,
    option3: false,
    // Add more options as needed
  });
  const [selectedMonth, setSelectedMonth] = useState(1);
  const [profileData, setProfileData] = useState("");
  const [barGraphData, setBarGraphData] = useState({});
  const [loading, setLoading] = useState(true);
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

  const handleMonthChange = (event) => {
    setSelectedMonth(event.target.value);
  };

  const handleCheckboxChange = (option) => {
    setCheckboxes((prevCheckboxes) => ({
      ...prevCheckboxes,
      [option]: !prevCheckboxes[option],
    }));
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://api.sgillabs.com/get_demand_plot_data"
        );
        // const data = JSON.parse(response.data);
        // setPlotData(data);
        const raw_data = response.data;
        setPlotData(raw_data);
      } catch (error) {
        console.error("Error fetching plot data:", error);
      }
    };

    const fetchMonthData = async () => {
      try {
        const response = await axios.post(
          "http://api.sgillabs.com/monthly_demand_profile",
          { selectedMonth, checkboxes }
        );
        const month_data = JSON.parse(response.data);
        setProfileData(month_data);
      } catch (error) {
        console.error("Error fetching plot data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    fetchMonthData();
  }, [selectedMonth, checkboxes]);

  useEffect(() => {
    if (plotData) {
      const PeakDaily = Object.values(plotData?.PeakDailyDemand);
      const MonthlyPeak = Object.values(plotData?.MonthlyPeakDemand);

      const data = [
        {
          x: plotData?.Month,
          y: PeakDaily,
          type: "bar",
          name: "PeakDailyDemand",
          marker: { color: "blue" },
        },
        {
          x: plotData?.Month,
          y: MonthlyPeak,
          type: "bar",
          name: "MonthlyPeakDemand",
          marker: { color: "orange" },
        },
      ];
      setBarGraphData(data);
    }
  }, [plotData]);

  const layout = {
    title: "Monthly Peak and Average Demand: ",
    xaxis: { title: "Month" },
    yaxis: { title: "Demand" },
    barmode: "stack", // Use 'group' for grouped bars
    height: "600",
  };

  if (loading) {
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
    </div>;
  } else {
    return (
      <div style={{ display: "flex" }}>
        <div
          style={{
            backgroundColor: "#4C4E5A",
            width: "25%",
            marginLeft: "20px",
          }}
        >
          <h3 style={{ fontSize: "30px", color: "white" }}>
            Load Profile Data:
          </h3>
          <h3
            style={{
              color: "white",
              fontSize: "30px",
              marginLeft: "20px",
              marginRight: "20px",
            }}
          >
            Select Options For Filtering:
          </h3>
          <select
            value={selectedMonth}
            onChange={handleMonthChange}
            style={{
              height: "8%",
              width: "85%",
              marginTop: "20px",
              marginBottom: "15px",
              marginRight: "20px",
              padding: "8px",
              fontSize: "16px",
              borderRadius: "4px",
              border: "1px solid #ccc",
              backgroundColor: "#fff",
              cursor: "pointer",
            }}
          >
            <option value="" disabled>
              Select a month
            </option>
            {months.map((month, index) => (
              <option key={index} value={index + 1}>
                {month}
              </option>
            ))}
          </select>
          <div style={{ display: "flex" }}>
            <input
              style={{ marginLeft: "30px" }}
              type="checkbox"
              checked={checkboxes.option1}
              onChange={() => handleCheckboxChange("option1")}
            />

            <label style={{ fontSize: "20px", color: "white" }}>
              Peak Daily Avg. Demand
            </label>
          </div>

          <div style={{ display: "flex" }}>
            <input
              style={{ marginLeft: "30px" }}
              type="checkbox"
              checked={checkboxes.option2}
              onChange={() => handleCheckboxChange("option2")}
            />
            <label
              style={{ fontSize: "20px", color: "white", marginRight: "20px" }}
            >
              Monthly Avg. Demand
            </label>
          </div>

          <div style={{ display: "flex" }}>
            <input
              style={{ marginLeft: "30px" }}
              type="checkbox"
              checked={checkboxes.option3}
              onChange={() => handleCheckboxChange("option3")}
            />
            <label
              style={{
                fontSize: "20px",
                color: "white",
                marginRight: "20px",
                marginBottom: "20px",
              }}
            >
              Peak Demand
            </label>
          </div>
        </div>
        <div style={{ marginLeft: "30px", maxwidth: "20%" }}>
          {profileData?.data ? (
            <PlotlyComponent
              data={profileData?.data}
              layout={profileData?.layout}
            />
          ) : (
            ""
          )}
        </div>
        <div style={{ marginLeft: "30px", maxwidth: "20%" }}>
          {barGraphData ? (
            <Plot data={barGraphData} layout={layout} />
          ) : (
            "Loading"
          )}
        </div>

        {/* <div style={{ marginLeft: "20px", width: "30%" }}>
          {plotData?.data ? (
            <PlotlyComponent data={plotData?.data} layout={plotData?.layout} />
          ) : (
            ""
          )}
        </div> */}
      </div>
    );
  }
};

export default DemandFilter;
