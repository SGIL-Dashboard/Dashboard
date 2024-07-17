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
import { assets } from "./UTILS/UTILS_Assets";
import { stylings } from "./UTILS/UTILS_STYLES";
const App = () => {
  const [theme , setTheme] = useState(localStorage.getItem("theme") !== "dark" ? "light" : "dark");
  React.useEffect(()=>
  {
    localStorage.setItem("theme" , theme);
  } , [theme]);
  return (<>
    <div className="App w-[100vw] h-[100vh] hidden lg:flex flex-col items-center overflow-x-hidden overflow-y-auto">
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
    <div className=" fixed w-[100vw] h-[100vh] top-0 left-0 z-[400] flex lg:hidden flex-col items-center justify-start gap-[2rem]">
      <div className="flex py-[1rem] gap-[1rem] items-center justify-center">
      <img src={assets.logo} alt="img" className=' w-[3rem]'/>
      <div className=" flex flex-col items-start">
     <span  className={`${stylings[theme].navbar.text} text-[1rem]`}>Smart Grid Interdependencies Laboratory</span>
     <span  className={`${stylings[theme].navbar.text} text-[1rem]`}>SGIL Load Analysis and Battery Sizing (LABS)</span>
      </div>
      </div>
      <div className="flex flex-col flex-grow items-center justify-center">
        <span className=" text-[1rem] font-bold text-blue-900">Mobile View Not Available</span>
        <span className=" text-[0.7rem] text-blue-900">Please Shift To Desktop View To Access This Page</span>
      </div>
    </div>
    </>
  );
};

export default App;
