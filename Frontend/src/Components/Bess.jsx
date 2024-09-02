import React, { useEffect, useState } from "react";
import "./Bess.css"; // Import the CSS file
import axios from "axios";
import Plot from "react-plotly.js";
import HoverTooltip from './HoverTooltip';
const Bess = () => {
  const [bessOut, setBessOut] = useState({});
  const [month3Data, setMonth3Data] = useState({});
  const [daily3Data, setDaily3Data] = useState({});
  const [loading, setLoading] = useState(true);
  const [inputs, setInputs] = useState({
    floatInput1: 24.25,
    floatInput2: 0,
    floatInput3: 967.5,
    floatInput4: 0,
    selectInput: 4,
    depthDischarge: 15,
    footprint: 37,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // If the input is the selectInput, convert the value to a number
    let newValue = value; 

    // If the input is the selectInput, convert the value to a number
    //  const newValue = name === "selectInput" ? parseInt(value, 10) : value;

    if (name === "selectInput") {
      newValue = parseInt(value, 10);
    } else if (name === "depthDischarge" || name === "footprint") {
      // Ensure values for depthDischarge and footprint are between 1 and 100
      newValue = Math.min(Math.max(parseInt(value, 10), 1), 100);
    }

    setInputs((prevInputs) => ({
      ...prevInputs,
      [name]: newValue,
    }));
  };

  const calculateBess = async () => {
    setBessOut({});
    try {
      const response = await axios.post(
        "http://api.sgillabs.com/bess_calculation",
        { inputs }
      );
      setBessOut(response.data);
    } catch (error) {
      console.error("Error fetching  data:", error);
    }
  };

  const handleSubmit = () => {
    // Perform any logic you need when the user submits the form

    // This effect will run only when the user clicks the submit button

    calculateBess();
  };

  useEffect(() => {
    calculateBess();
  }, []);

  useEffect(() => {
    const fetch3dMonthlyData = async () => {
      try {
          const response = await axios.get(
            "http://api.sgillabs.com/give_comp_3D_monthly_plot"
          );
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
          "http://api.sgillabs.com/give_comp_3D_daily_plot"
        );
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

  return (
    <div>
      <div
        style={{
          justifyContent: "space-between",
          margin: "auto",
          display: "flex",
          marginTop: "15px",
          marginBottom: "25px",
        }}
      >
        <div
          style={{
            backgroundColor: "rgb(76,78,90)",

            marginLeft: "20px",
            borderRadius: "5px",
            width: "20%",
            height: "150px",  
          }}
        >
          <h1 style={{ color: "white" }}>BESS Capacity(kWh):</h1>
          {/* <h1 style={{ color: "white" }}> </h1> */}
          <h1 style={{ color: "white" }}>
            {bessOut?.BESS_capacity ? bessOut?.BESS_capacity : ""}
          </h1>
        </div>
        <div
          style={{
            backgroundColor: "rgb(76,78,90)",
            marginRight: "20px",
            marginLeft: "15px",
            borderRadius: "5px",
            width: "20%",
            height: "150px",
          }}
        >
          <h1 style={{ color: "white" }}>BESS Cost ($):</h1>
          {/* <h1 style={{ color: "white" }}> Cost:</h1> */}
          <h1 style={{ color: "white" }}>
            {bessOut?.BESS_cost ? bessOut?.BESS_cost : ""}
          </h1>
        </div>
        <div
          style={{
            backgroundColor: "rgb(76,78,90)",
            marginRight: "20px",
            marginLeft: "15px",
            borderRadius: "5px",
            width: "20%",
            height: "150px",
          }}
        >
          <h1 style={{ color: "white" }}>BESS Footprint(cm^2):</h1>
          {/* <h1 style={{ color: "white" }}>Footprint:</h1> */}
          <h1 style={{ color: "white" }}>
            {bessOut?.BESS_footprint ? bessOut?.BESS_footprint : ""}
          </h1>
        </div>
        <div
          style={{
            backgroundColor: "rgb(76,78,90)",
            marginLeft: "15px",
            borderRadius: "5px",
            width: "20%",
            height: "150px",
          }}
        >
          <h1 style={{ color: "white" }}>BESS Power(kW):</h1>
          {/* <h1 style={{ color: "white" }}> Power:</h1> */}
          <h1 style={{ color: "white" }}>
            {bessOut?.BESS_power ? bessOut?.BESS_power : ""}
          </h1>
        </div>
      </div>
      <div style={{ display: "flex" }}>
        <div
          style={{
            marginLeft: "20px",
            backgroundColor: "#4C4E5A",
            width: "25%",
          }}
        >
          <form style={{ display: "flex", flexDirection: "column" }}>
            <div style={{ marginBottom: "10px" }}>
              <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
                BESS Depth of Discharge
              </label>
              <input
                style={{ flex: "1", marginLeft: "10px", minWidth: "4px" }}
                type="number"
                name="depthDischarge"
                value={inputs.depthDischarge}
                onChange={handleInputChange}
              />
            </div>

            <div style={{ marginBottom: "10px" }}>
              <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
                BESS Footprint (in^2/ kWh):
              </label>
              <input
                style={{ flex: "1", marginLeft: "10px", minWidth: "4px" }}
                type="number"
                name="footprint"
                value={inputs.footprint}
                onChange={handleInputChange}
              />
            </div>

            <div style={{ marginBottom: "10px" }}>
              <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
                BESS Capital Costs ($/kWh):
              </label>
              <input
                style={{ flex: "1", marginLeft: "10px", minWidth: "4px" }}
                type="number"
                name="floatInput1"
                value={inputs.floatInput1}
                onChange={handleInputChange}
              />
            </div>

            <div style={{ marginBottom: "10px" }}>
              <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
                BESS Capital Costs ($/kW):
              </label>
              <input
                style={{ flex: "1", marginLeft: "10px", minWidth: "4px" }}
                type="number"
                name="floatInput2"
                value={inputs.floatInput2}
                onChange={handleInputChange}
              />
            </div>

            <div style={{ marginBottom: "10px" }}>
              <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
                BESS O&M Costs ($/kWh):
              </label>
              <input
                style={{ flex: "1", marginLeft: "10px", minWidth: "4px" }}
                type="number"
                name="floatInput3"
                value={inputs.floatInput3}
                onChange={handleInputChange}
              />
            </div>

            <div style={{ marginBottom: "10px" }}>
              <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
                BESS O&M Costs ($/year):
              </label>
              <input
                style={{ flex: "1", marginLeft: "10px", minWidth: "4px" }}
                type="number"
                name="floatInput4"
                value={inputs.floatInput4}
                onChange={handleInputChange}
              />
            </div>

            <div style={{ marginBottom: "10px" }}>
              <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
                Battery Duration:
              </label>
              <select
                style={{
                  flex: "1",
                  marginLeft: "10px",
                  width: "37%",
                  height: "23px",
                  minWidth: "1px",
                }}
                name="selectInput"
                value={inputs.selectInput}
                onChange={handleInputChange}
              >
                {[0, 1, 2, 3, 4].map((option) => (
                  <option key={option} value={option}>
                    {option} Hours
                  </option>
                ))}
              </select>
            </div>

            <button type="button" onClick={handleSubmit}>
              Submit
            </button>
          </form>
        </div>

        <div style={{ marginLeft: "5%", margin: "auto" }}>
          {month3Data?.data ? (
            <Plot data={month3Data.data} layout={month3Data.layout} />
          ) : (
            ""
          )}
        </div>
        <div style={{ marginLeft: "5%", margin: "auto" }}>
          {daily3Data?.data ? (
            <Plot data={daily3Data.data} layout={daily3Data.layout} />
          ) : (
            ""
          )}
        </div>
      </div>
    </div>
  );
};

export default Bess;
