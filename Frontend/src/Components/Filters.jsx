import React, { useState, useEffect } from "react";
import Select from "react-select";

const options = [
  { value: "Sunday", label: "Sunday" },
  { value: "Monday", label: "Monday" },
  { value: "Tuesday", label: "Tuesday" },
  { value: "Wednesday", label: "Wednesday" },
  { value: "Thursday", label: "Thursday" },
  { value: "Friday", label: "Friday" },
  { value: "Saturday", label: "Saturday" },
];

const MultiSelectDropdown = () => {
  const handleChange = (selectedOptions) => {
    // Do something with the selected days, e.g., filter data
  };

  return (
    <div
      style={{
        height: "20%",
        width: "100%",
        display: "flex",
        flexDirection: "column", // Set flexDirection to column
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <h2
        style={{
          color: "green",
          marginBottom: "10px",
          fontSize: "30px",
          display: "block",
        }}
      >
        Select Days of the Week
      </h2>
      <Select
        isMulti
        options={options}
        onChange={handleChange}
        placeholder="Select days..."
      />
    </div>
  );
};

const Filters = () => {
  

  return (
    <div>
      <MultiSelectDropdown />
      
    </div>
  );
};

export default Filters;
