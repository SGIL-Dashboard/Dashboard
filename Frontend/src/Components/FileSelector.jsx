import React, { useEffect } from "react";
import axios from "axios";
import { useState } from "react";

import NumbersData from "./NumbersData/NumbersData";
import Charts_handling from "./Charts_handling/Charts_handling";
import { assets } from "../UTILS/UTILS_Assets";
import SVGComponent from "./SVGS/SVGS";
import {calcLength, motion} from "framer-motion"
import Popup from "./Popup/Popup";
import { getUniqueId, handleFileCheck, makeApiRequest } from "../UTILS/UTILS_HELPERS";
import toast from "react-hot-toast";
import { stylings } from "../UTILS/UTILS_STYLES";
import { globalContext } from "../Context/Context";
import { useContext } from "react";
import FinancialAnalysis from "./Financial_Analysis/Financial_Analysis";
const FileSelector = () => {
  const {theme} = useContext(globalContext);
  const [selectedOption, setSelectedOption] = useState("Administration Building.xlsx");
  const [selectedInstance , setSelectedInstance] = useState("Administration Building.xlsx");
  const [toggle , setToggle] = useState(false);
  const [fileData, setFileData] = useState([]);
  const [expandImg , setExpandImg] = useState(false);

  const [dataInput , setDataInput] = useState({name : "" , file : ""});
  const [selectionUpdated, setSelectionUpdated] = useState(false);
  const [rollDown , setRollDown] = useState(false);
  const [uploadFileUnderProcess , setUploadFileUnderProcess] = useState(false);
  const [dfData, setDfData] = useState();
  const [fName , setFName] = useState("");
  const [bessCost , setBessCost] = React.useState("");
  const [bessPower , setBessPower] = React.useState("");
  const handleDropdownChange = (event) => {
    setSelectedOption(event.target.value);
  };
  const handleFileChange = (event) => {
    const files = event.target.files;
    // Process the selected files or get the list of filenames
    const filenames = Array.from(files).map((file) => file.name);
    console.log(filenames);
  };
  const fetchData = async () => {
    try {
      const response = await axios.get("https://api.sgillabs.com/get_all_files");
      const data = response.data.all_file;
      console.log("dataof file", data);
      setFileData(data);
    } catch (error) {
      console.error("Error fetching  data:", error);  
    }
  };
  const fileName = async () => {
    try {
      setDfData("");
      const response = await axios.post(
        "https://api.sgillabs.com/file_selection",
        { selectedOption , UID : getUniqueId() }
      );
      console.log(response, selectedOption);
      setDfData(response.data.status);
      setSelectionUpdated(true);
      // window.location.reload();
    } catch (error) {
      console.error("Error fetching  data:", error);
    }
  };

  useEffect(() => {
    setSelectionUpdated(false);
    fetchData();
    fileName();
  }, [selectedOption]);
  const handleSubmit = async()=>
  {
    const errors = {}
    if(!dataInput.name)
    {
      toast.error("please enter valid name for file");
      return;
    }
    else if(!dataInput.file)
    {
      toast.error("please enter a xlsx file");
      return
    }
    try
    {
      setUploadFileUnderProcess(true);
      const {data , error} = await makeApiRequest({method : "post" , urlPath : "file_selection" , body : {name : dataInput.name , file : dataInput.file , UID : getUniqueId()} , convertToFormData : true});
      if(data)
      {
        
        toast.success("your file uploaded successfully");
        // setToggle(false);
        // setFName("");
        // setDataInput({name : "" , file : ""});
        setSelectedOption(dataInput.name);
        setSelectionUpdated(true);
      }
      else
      {
        toast.error("Error uploading file , please try again later");
      }
      setUploadFileUnderProcess(false);
    }
    catch(e)
    {
      setUploadFileUnderProcess(false);
      toast.error("Error uploading file , please try again later");
    }
  }
  return (
    <div className=" w-full flex flex-col">
      <div className={stylings[theme].introSection.parent}>
      <div className=" w-full h-fit flex  py-[3rem] items-center justify-evenly shrink-0">
        <div className="flex w-1/2 flex-col items-start h-full justify-start">  
          <h1 className={stylings[theme].introSection.heading}>
            {`Building Load Profile Analysis for `}<span className=" whitespace-nowrap">{selectedOption.split(".xlsx")[0]}</span>
          </h1>
          {/* <h1 className={stylings[theme].introSection.heading}>
          Battery Energy Storage Sizing
          </h1> */}
        </div>
        {expandImg ? <Popup onClose={()=>
          {
            setExpandImg(false);
          }}><div className=" w-[50%] top-[50%] left-[50%] absolute translate-x-[-50%] translate-y-[-50%] h-fit shrink-0"><img src={assets[selectedOption.split(".xlsx")[0].replaceAll(" " , "_").replaceAll("-" , "_")]} alt="img" className=" w-[100%] h-full object-contain"></img></div></Popup> : <></>}
        <div className="w-[33rem] gap-[2rem] shrink-0 overflow-y-visible overflow-x-clip flex items-start justify-center flex-col">
          <div className={stylings[theme].introSection.fileSelectorPack.toggleContainer}>
            <motion.div variants={{right : {right : 0 , left : "auto"} , left  : {left : 0 , right : "auto"}}} animate={toggle ? "right" : "left"} className={stylings[theme].introSection.fileSelectorPack.toggleBg}></motion.div>
            <button style={{color : !toggle ? "white" : undefined}} onClick={()=>
              {
                setToggle(false);
              }} className={stylings[theme].introSection.fileSelectorPack.button}>CCNY Buildings</button>
            <button style={{color : toggle ? "white" : undefined}} onClick={()=>
              {
                setToggle(true)
              }} className={`${stylings[theme].introSection.fileSelectorPack.button} border-r-[0rem]`}>Upload Your Own</button>
          </div>
          <div style={{transform : `translateX(${toggle ? "-50%" : 0})`}} className=" w-[200%] duration-200 ease-in-out h-fit shrink-0 flex items-center justify-start">
          <div className=" w-[50%] shrink-0 gap-[1rem] flex items-center justify-center">
         <img onClick={()=>
          {
            setExpandImg(true);
            console.log({val : selectedInstance.split(".xlsx")[0].replaceAll(" " , "_").replaceAll("-" , "_")})
          }} src={assets[selectedInstance.split(".xlsx")[0].replaceAll(" " , "_").replaceAll("-" , "_")]} alt="img" className=" w-[5rem] cursor-pointer h-[5rem] rounded-full object-cover"/>
         <div 
            className={stylings[theme].introSection.fileSelectorPack.selectionOptionDiv}
          >
            <button onClick={()=>
              {
                setRollDown(!rollDown);
              }} className="w-full h-full pl-[1rem] shrink-0 flex items-center justify-between">
              <span className={stylings[theme].introSection.fileSelectorPack.selectedFile}>
                {selectedInstance.split(".xlsx")[0]}
              </span>
              <span className=" ease-in-out duration-300" style={{transform  : `rotate(${!rollDown ? 0 : 90}deg)`}}><SVGComponent {...stylings[theme].introSection.fileSelectorPack.rollDownSvg}
              /></span>
            </button>
            <motion.div tabIndex={-1}
          onBlur={()=>
            {
              setRollDown(false);
            }} variants={{rollDown : {height : `30rem` , transition : {staggerChildren : 0.1 , type : "tween"}} , rollUp : {height : 0}}} animate = {rollDown ? "rollDown" : "rollUp"} className={stylings[theme].introSection.fileSelectorPack.rollDownContainer}>
              {fileData.map((val)=>
              {
                console.log({cal : val.split(".xlsx")[0].replaceAll([" "] , "_")})
                return<motion.button variants={{rollDown : {opacity:1 , x : 0 } , rollUp : {opacity : 0 , x : 50}}} onClick={()=>
                  {
                    setSelectedOption(val);
                    setSelectedInstance(val);
                    setRollDown(false);
                  }} className={stylings[theme].introSection.fileSelectorPack.containerToBeSelected}><img src={assets[val.split(".xlsx")[0].replaceAll([" "] , "_").replaceAll("-" , "_")]} alt={assets.no_image} className=" w-[3rem] h-[3rem] rounded-full" /><span>{val.split(".xlsx")[0]}</span></motion.button>
              })}
            </motion.div>
          </div>
          
         </div>
          <form onSubmit={(e)=>{e.preventDefault()}} className=" w-[50%] h-[5rem] shrink-0 gap-[1rem] flex justify-center items-center">
            <div className=" relative w-[30%]">
              <input value={dataInput.name} onChange={(e)=>
                {
                  setDataInput({...dataInput , name : e.target.value});
                }} placeholder=" " type="text" id="alias" className={stylings[theme].introSection.fileSelectorPack.form.input}/>
              <label htmlFor="alias" className={stylings[theme].introSection.fileSelectorPack.form.label}>Name</label>
            </div>
            <div className=" w-[30%] shrink-0">
              <label htmlFor="fileForUpload" className={stylings[theme].introSection.fileSelectorPack.form.selectLabel}>{fName ? fName : "Choose File"}</label>
              <input type= "file" className="hidden" onChange={(e)=>
                {
                  if(handleFileCheck(e.target.files[0]))
                  {
                    setDataInput({...dataInput , file : e.target.files[0]});
                    setFName(e.target.files[0].name)
                  }
                }} id="fileForUpload" />
            </div>
            <button onClick={()=>
              {
                if(!uploadFileUnderProcess)
                {
                  setSelectionUpdated(false);
                  handleSubmit();
                }
              }} className={`${stylings[theme].introSection.fileSelectorPack.form.button}`}>{uploadFileUnderProcess ? <div className=" w-[1.7rem] h-[1.7rem] rounded-full shrink-0 border-[0.1rem] border-y-blue-900 border-x-white animate-spin"></div> : "Submit"}</button>
         </form>
          </div>
          {/* <select
         className="text-[1.3rem] text-blue-900 bg-blue-300 border-[0.15rem] rounded-md px-[1rem] py-[.1rem] border-blue-900"
          id="dropdown"
          onChange={handleDropdownChange}
          value={selectedOption || ""}
        >
          <option value="" disabled>
            Select an option
          </option>
          {fileData.map((item, index) => (
            <option key={index} value={item} className=" flex items-center justify-center">
              <img src={assets[item.split(".xlsx")[0]]} alt={assets.no_image} /><span>{item}</span>
            </option>
          ))}
        </select> */}

        </div>
      </div>
      <div className=" w-full h-[4rem] flex items-start gap-[.2rem]">
        <img src={assets.buildingsBG} alt="img" className=" w-[25%] h-full" />
        <img src={assets.buildingsBG1} alt="img" className=" w-[25%] h-full" />
        <img src={assets.buildingsBG2} alt="img" className=" w-[25%] h-full" />
        <img src={assets.buildingsBG3} alt="img" className=" w-[25%] h-full" />
        {/* <img src={assets.buildingsBG} alt="img" className=" w-[10%] h-full" />
        <img src={assets.buildingsBG1} alt="img" className=" w-[10%] h-full" />
        <img src={assets.buildingsBG2} alt="img" className=" w-[10%] h-full" />
        <img src={assets.buildingsBG3} alt="img" className=" w-[10%] h-full" />
        <img src={assets.buildingsBG} alt="img" className=" w-[10%] h-full" />
        <img src={assets.buildingsBG1} alt="img" className=" w-[10%] h-full" /> */}
      </div>
      </div>
      {/* <label htmlFor="fileInput">Select files: </label>
      <input type="file" accept=".xls,.xlsx"/>   */}
      <div
        style={{
          backgroundColor: "#4C4E5A",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        {/* {selectedOption && (
          <h1
            style={{ color: "white", fontSize: "15px", marginBottom: "30px" }}
          >
            Selected option: {selectedOption}
          </h1>
        )} */}
      </div>
      <NumbersData selectionUpdated={selectionUpdated} setBessPower = {setBessPower} setBessCost={setBessCost}/>
      <Charts_handling
        selectedOption={selectedOption}
        selectionUpdated={selectionUpdated}
      />
      <FinancialAnalysis bessPower = {bessPower} bessCost={bessCost}/>
    </div>
  );
};

export default FileSelector;
