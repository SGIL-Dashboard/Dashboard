import React, { useEffect, useState } from "react";
import "./Bess.css"; // Import the CSS file
import axios from "axios";

const Bess = () => {
  const [bessOut, setBessOut] = useState({});

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
        "http://54.175.34.126:8000/bess_calculation",
        { inputs }
      );
      // console.log(response.data);
      setBessOut(response.data);
    } catch (error) {
      console.error("Error fetching  data:", error);
    }
  };

  const handleSubmit = () => {
    // Perform any logic you need when the user submits the form
    console.log("Form submitted:", inputs);
    // This effect will run only when the user clicks the submit button
    console.log("Effect triggered:", inputs);

    calculateBess();
  };

  useEffect(() => {
    calculateBess();
  }, []);

  return (
    <div style={{ display: "flex" }}>
      <div
        style={{ marginLeft: "20px", backgroundColor: "#4C4E5A", width: "25%" }}
      >
        <form style={{ display: "flex", flexDirection: "column" }}>
          <div style={{ display: "flex", marginBottom: "10px" }}>
            <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
              BESS Depth of Discharge (%):
            </label>
            <input
              style={{ flex: "1", marginLeft: "10px" }}
              type="number"
              name="depthDischarge"
              value={inputs.depthDischarge}
              onChange={handleInputChange}
            />
          </div>

          <div style={{ display: "flex", marginBottom: "10px" }}>
            <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
              BESS Footprint (cm^2/ kWh):
            </label>
            <input
              style={{ flex: "1", marginLeft: "10px" }}
              type="number"
              name="footprint"
              value={inputs.footprint}
              onChange={handleInputChange}
            />
          </div>

          <div style={{ display: "flex", marginBottom: "10px" }}>
            <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
              BESS Capital Costs ($/kWh):
            </label>
            <input
              style={{ flex: "1", marginLeft: "10px", width: "auto" }}
              type="number"
              name="floatInput1"
              value={inputs.floatInput1}
              onChange={handleInputChange}
            />
          </div>

          <div style={{ display: "flex", marginBottom: "10px" }}>
            <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
              BESS Capital Costs ($/kW):
            </label>
            <input
              style={{ flex: "1", marginLeft: "10px" }}
              type="number"
              name="floatInput2"
              value={inputs.floatInput2}
              onChange={handleInputChange}
            />
          </div>

          <div style={{ display: "flex", marginBottom: "10px" }}>
            <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
              BESS O&M Costs ($/kWh):
            </label>
            <input
              style={{ flex: "1", marginLeft: "10px" }}
              type="number"
              name="floatInput3"
              value={inputs.floatInput3}
              onChange={handleInputChange}
            />
          </div>

          <div style={{ display: "flex", marginBottom: "10px" }}>
            <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
              BESS O&M Costs ($/year):
            </label>
            <input
              style={{ flex: "1", marginLeft: "10px" }}
              type="number"
              name="floatInput4"
              value={inputs.floatInput4}
              onChange={handleInputChange}
            />
          </div>

          <div style={{ display: "flex", marginBottom: "10px" }}>
            <label style={{ flex: "1", color: "white", fontSize: "20px" }}>
              Battery Duration:
            </label>
            <select
              style={{ flex: "1", marginLeft: "10px" }}
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

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          margin: "auto",
        }}
      >
        <div
          style={{
            backgroundColor: "rgb(76,78,90)",
            marginRight: "20px",
            borderRadius: "5px",

            flex: 1,
          }}
        >
          <h1 style={{ color: "white" }}>BESS </h1>
          <h1 style={{ color: "white" }}> Capacity:</h1>
          <h1 style={{ color: "white" }}>
            {bessOut?.BESS_capacity ? bessOut?.BESS_capacity : ""}
          </h1>
        </div>
        <div
          style={{
            backgroundColor: "rgb(76,78,90)",
            marginRight: "20px",
            borderRadius: "5px",

            flex: 1,
          }}
        >
          <h1 style={{ color: "white" }}>BESS </h1>
          <h1 style={{ color: "white" }}> Cost:</h1>
          <h1 style={{ color: "white" }}>
            {bessOut?.BESS_cost ? bessOut?.BESS_cost : ""}
          </h1>
        </div>
        <div
          style={{
            backgroundColor: "rgb(76,78,90)",
            marginRight: "20px",
            borderRadius: "5px",

            flex: 1,
          }}
        >
          <h1 style={{ color: "white" }}>BESS </h1>
          <h1 style={{ color: "white" }}>Footprint:</h1>
          <h1 style={{ color: "white" }}>
            {bessOut?.BESS_footprint ? bessOut?.BESS_footprint : ""}
          </h1>
        </div>
        <div
          style={{
            backgroundColor: "rgb(76,78,90)",
            marginRight: "20px",
            borderRadius: "5px",

            flex: 1,
          }}
        >
          <h1 style={{ color: "white" }}>BESS </h1>
          <h1 style={{ color: "white" }}> Power:</h1>
          <h1 style={{ color: "white" }}>
            {bessOut?.BESS_power ? bessOut?.BESS_power : ""}
          </h1>
        </div>
      </div>
    </div>
  );
};

export default Bess;
