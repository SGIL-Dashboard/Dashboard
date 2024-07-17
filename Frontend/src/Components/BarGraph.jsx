import React from "react";
import Plotly from "react-plotly.js";

const BarGraph = () => {
  // Sample data for illustration purposes
  const categories = ["Category A", "Category B", "Category C"];
  const values1 = [30, 45, 20];
  const values2 = [15, 25, 10];

  const data = [
    {
      x: categories,
      y: values1,
      type: "bar",
      name: "Group 1",
      marker: { color: "blue" },
    },
    {
      x: categories,
      y: values2,
      type: "bar",
      name: "Group 2",
      marker: { color: "orange" },
    },
  ];
  const layout = {
    title: "Stacked Bar Graph Example",
    xaxis: { title: "Categories" },
    yaxis: { title: "Values" },
    barmode: "stack", // Use 'group' for grouped bars
  };

  return (
    <Plotly
      data={[
        {
          x: categories,
          y: values1,
          type: "bar",
          name: "Group 1",
          marker: { color: "blue" },
        },
        {
          x: categories,
          y: values2,
          type: "bar",
          name: "Group 2",
          marker: { color: "orange" },
        },
      ]}
      layout={layout}
      style={{ width: "100%", height: "400px" }}
    />
  );
};

export default BarGraph;
