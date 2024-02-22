import "./App.css";
import PlotComponent from "./Components/PlotComonent";
import DateRangePicker from "./Components/DateRangePicker";
import Filters from "./Components/Filters";
import DemandFilter from "./Components/DemandFilter";
import React, { useState } from "react";
import FileSelector from "./Components/FileSelector";
import BarGraph from "./Components/BarGraph";
import Navbar from "./Components/Navbar/Navbar";
import { globalContext } from "./Context/Context";
import { Toaster } from "react-hot-toast";
const App = () => {
  const [theme , setTheme] = useState(localStorage.getItem("theme") !== "dark" ? 'light' : "dark");
  React.useEffect(()=>
  {
    localStorage.setItem("theme" , theme);
  } , [theme]);
  return (
    <div className="App w-[100vw] h-[100vh] flex flex-col items-center overflow-x-hidden overflow-y-auto">
      <globalContext.Provider value={{theme , setTheme}}>
      <Toaster/>
      <Navbar/>
      <FileSelector />
      </globalContext.Provider>
      {/* <BarGraph /> */}
      {/* <div style={{ marginBottom: "80px", color: "green" }}>
        <Filters />
      </div> */}
      {/* <DateRangePicker
        style={{ marginBottom: "50px", color: "green", textAlign: "center" }}
      /> */}
    </div>
  );
};

export default App;
