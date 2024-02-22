export const stylings = {
 light : 
 {
  navbar : {
   container : "w-full bg-blue-100 h-fit shrink-0 flex items-center justify-between px-[1rem] py-[.5rem]",
   text : "text-[2.5rem] font-bold text-blue-800",
   svg : {selector : "moon" , width : "w-[1.5rem]"},
  },
  introSection : {
   parent : "w-full introSection h-fit flex bg-slate-100 flex-col",
   heading : "text-[1.7rem] text-start text-blue-900 font-bold",
   fileSelectorPack :{
    toggleContainer : "w-full relative overflow-hidden h-fit shrink-0 flex border-[0.1rem] border-blue-900 rounded-xl",
    toggleBg : " w-1/2 bg-blue-900 z-[0] h-full top-0 absolute",
    button : "w-1/2 relative z-[1] text-blue-900  text-[1.1rem] py-[.1rem] border-r-[0.1rem] border-blue-900",
    selectionOptionDiv : `w-[20rem] h-[3rem] relative shrink-0 flex flex-col items-center justify-center 
    overflow-visible border-b-[0.1rem] border-blue-900`,
    selectedFile : "text-[1.2rem] text-blue-900",
    rollDownContainer : "absolute bg-gray-100 w-full z-[15] top-[100%] left-0 flex overflow-x-hidden overflow-y-auto shrink-0 flex-col items-start justify-start",
    containerToBeSelected : " w-full h-[3.7rem] hover:bg-slate-200 shrink-0 border-b-[0.1rem] border-b-slate-200 flex items-center justify-between px-[1rem]",
    rollDownSvg : {selector : "down" , width : "w-[1.5rem]" , color : "#1E3A8A"},
    form:{input : " outline-none w-full text-blue-900 styledTextInputs text-[1.1rem] border-b-[0.1rem] border-blue-900 bg-transparent",
    label : "absolute text-[1rem]",
    selectLabel : "flex rounded-md w-full items-center justify-center py-[.2rem] shrink-0 border-[0.1rem] border-blue-900",
    button : "w-[30%] h-[2rem] flex items-center justify-center border-[0.1rem] bg-blue-900 text-white border-blue-900 py-[0.2rem]"
   }
   }
  },
  calculation : {
   parent : "w-full h-fit shrink-0 flex border-b-[0.1rem] border-slate-200 justify-evenly py-[4rem]",
   subParent : "w-[60%] border-r-[0.1rem] border-slate-200 px-[3rem] h-fit flex-col justify-between flex",
   rangeParent : "flex items-start justify-start flex-col",
   rangeInput : "styledRange w-full",
   floatInput : " outline-none bg-transparent  text-[1.5rem] shrink-0 border-b-[0.15rem] duration-300 ease-in-out border-blue-900",
   submitButton : "text-[1.2rem] outline-none flex items-center justify-center hover:bg-blue-900 hover:text-white ease-in-out duration-100 text-blue-900 border-[0.1rem] h-[2.4rem] rounded-md w-[8rem] border-blue-900",
   value : "text-[1.9rem] text-blue-900 font-bold"
  },
  chartSelection : {
   parent : " w-full flex items-start justify-between",
   chartSelectorContainer : {
    parent : "bg-slate-100 w-[30%] flex flex-col items-center justify-center ml-[.7rem] mt-[.7rem] pt-[.7rem]",
    button : {selected : "bg-gradient-to-l from-blue-200 to-blue-100 w-full py-[1.2rem] border-b-[0.1rem] border-blue-900 pl-[.7rem] flex items-center justify-start" , notSelected : "hover:bg-gradient-to-l from-transparent to-blue-200 w-full py-[1.2rem] border-b-[0.1rem] border-blue-900 pl-[.7rem] flex items-center justify-start"},
    span : "text-[1.1rem] text-blue-900 font-semibold",
    form : {
     select : "bg-transparent text-[1.1rem] w-[8rem] outline-none border-b-[.1rem] border-blue-900",
     label : " m-0"
    }
   }
  }
 },
 dark : {
  navbar : {
   container : "w-full bg-black h-fit shrink-0 flex items-center justify-between px-[1rem] py-[.5rem]",
   text : "text-[2.5rem] font-bold text-white",
   svg : {selector : "sun" , width : "w-[1.5rem]" , color : "white" },
  },
  introSection : {
   parent : "w-full introSection h-fit flex bg-slate-600 flex-col",
   heading : "text-[1.7rem] text-start text-white font-bold",
   fileSelectorPack :{
    toggleContainer : "w-full relative overflow-hidden h-fit shrink-0 flex border-[0.1rem] border-slate-500 rounded-xl",
    toggleBg : " w-1/2 bg-slate-500 z-[0] h-full top-0 absolute",
    button : "w-1/2 relative z-[1] text-white  text-[1.1rem] py-[.1rem] border-r-[0.1rem] border-slate-500",
    selectionOptionDiv : `w-[20rem] h-[3rem] relative shrink-0 flex flex-col items-center justify-center 
    overflow-visible border-b-[0.1rem] border-white`,
    selectedFile : "text-[1.2rem] text-white",
    rollDownContainer : "absolute bg-slate-600 w-full z-[15] top-[100%] left-0 flex overflow-x-hidden overflow-y-auto shrink-0 flex-col items-start justify-start",
    containerToBeSelected : " text-white w-full h-[3.7rem] hover:bg-slate-500 shrink-0 border-b-[0.1rem] border-b-slate-200 flex items-center justify-between px-[1rem]",
    rollDownSvg : {selector : "down" , width : "w-[1.5rem]" , color : "white"},
    form:{input : " outline-none w-full text-white styledTextInputs text-[1.1rem] border-b-[0.1rem] border-white bg-transparent",
    label : "absolute text-[1rem] text-white",
    selectLabel : "flex rounded-md w-full items-center justify-center text-white py-[.2rem] shrink-0 border-[0.1rem] border-white",
    button : "w-[30%] flex items-center justify-center border-[0.1rem] bg-slate-500 text-white border-slate-500 py-[0.2rem]"
   }
   }
  },
  calculation : {
   parent : "w-full h-fit shrink-0 flex border-b-[0.1rem] bg-gray-800 border-slate-200 justify-evenly py-[4rem]",
   subParent : "w-[60%] border-r-[0.1rem] border-slate-200 px-[3rem] h-fit flex-col justify-between flex",
   rangeParent : "flex items-start justify-start flex-col text-white",
   rangeInput : "styledRangeDark w-full",
   floatInput : " outline-none bg-transparent text-white text-[1.5rem] shrink-0 border-b-[0.15rem] duration-300 ease-in-out border-white",
   submitButton : "text-[1.2rem] outline-none flex items-center justify-center hover:bg-gray-700 hover:text-white ease-in-out duration-100 text-white border-[0.1rem] h-[2.4rem] rounded-md w-[8rem] border-white",
   value : "text-[1.9rem] text-white font-bold"
  },
  chartSelection : {
   parent : " w-full flex items-start justify-between bg-gray-800",
   chartSelectorContainer : {
    parent : "bg-gray-700 w-[30%] flex flex-col items-center justify-center ml-[.7rem] mt-[.7rem] pt-[.7rem]",
    button : {selected : "bg-gradient-to-l from-gray-600 to-gray-600 w-full py-[1.2rem] border-b-[0.1rem] border-gray-400 pl-[.7rem] flex items-center justify-start" , notSelected : "hover:bg-gradient-to-l from-gray-600 to-gray-600 w-full py-[1.2rem] border-b-[0.1rem] border-gray-400 pl-[.7rem] flex items-center justify-start"},
    span : "text-[1.1rem] text-gray-400 font-semibold",
    form : {
     select : "bg-gray-800 text-white text-[1.1rem] w-[8rem] outline-none border-b-[.1rem] border-white",
     label : " m-0 text-white"
    }
   }
  }
 }
}