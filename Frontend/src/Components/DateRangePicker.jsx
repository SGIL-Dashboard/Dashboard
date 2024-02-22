// DateRangePicker.js

import React, { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./DateRangePicker.css"; // Import the CSS file
import axios from "axios";
import Plotly from "plotly.js/lib/core";
import createPlotlyComponent from "react-plotly.js/factory";
const PlotlyComponent = createPlotlyComponent(Plotly);

const DateRangePicker = () => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [monthData, setMonthData] = useState({});

  const handleStartDateChange = (date) => {
    setStartDate(date);
  };

  const handleEndDateChange = (date) => {
    setEndDate(date);
  };

  useEffect(() => {
    const fetchMonthData = async () => {
      try {
        const response = await axios.post(
          "http://localhost:5000/fig_monthly_Demand_data",
          { startDate, endDate }
        );
        const month_data = JSON.parse(response.data);
        setMonthData(month_data);
      } catch (error) {
        console.error("Error fetching plot data:", error);
      }
    };
    fetchMonthData();
  }, [endDate]);

  return (
    <div className="date-range-picker-container">
      <div className="date-picker-label">
        <label
          style={{
            marginRight: "10px",
            color: "green",
            fontSize: "25px",
            marginLeft: "20px",
          }}
        >
          Start Date:
        </label>
        <DatePicker
          selected={startDate}
          onChange={handleStartDateChange}
          selectsStart
          startDate={startDate}
          endDate={endDate}
          minDate={new Date("2019-01-01")}
          maxDate={new Date("2019-12-31")}
          className="custom-date-picker"
        />
      </div>
      <div className="date-picker-label">
        <label
          style={{
            color: "green",
            fontSize: "25px",
            marginLeft: "20px",
            marginRight: "20px",
          }}
        >
          End Date:
        </label>
        <DatePicker
          selected={endDate}
          onChange={handleEndDateChange}
          selectsEnd
          startDate={startDate}
          endDate={endDate}
          minDate={new Date("2019-01-01")}
          maxDate={new Date("2019-12-31")}
          className="custom-date-picker"
        />
      </div>
      <PlotlyComponent data={monthData.data} layout={monthData.layout} />
    </div>
  );
};

export default DateRangePicker;
