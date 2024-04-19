export const stylings = {
    light : 
    {
    toolTip : {left : "TT bg-[rgba(30,64,175,0.8)] py-[0.15rem] rounded-md border-[0.2rem] border-blue-400 px-[1rem] TTL" , middle : "TT bg-[rgba(30,64,175,0.6)] py-[0.15rem] rounded-md border-[0.2rem] border-blue-400 px-[1rem]"},
     navbar : {
      container : "w-full bg-blue-100 sticky top-0 z-[300] h-fit shrink-0 flex items-center justify-between px-[3rem] py-[1.2rem]",
      text : "text-[1.7rem] selectNone font-semibold text-blue-800",
    svg : {selector : "moon" , width : "w-[2.4rem]"},
     },
     introSection : {
        
      parent : "w-full introSection h-fit flex bg-slate-100 flex-col",
      heading : "text-[1.7rem]  text-start selectNone text-blue-800 font-semibold",
      fileSelectorPack :{
        selectedFileContainer  :" w-full border-b-[0.1rem] pb-[.5rem] border-blue-900 shrink-0 px-[1rem] gap-[1rem] flex items-center justify-between", 
       toggleContainer : "w-full relative overflow-hidden h-fit shrink-0 flex border-[0.1rem] border-blue-900 rounded-xl",
       toggleBg : " w-1/2 bg-blue-900 z-[0] h-full top-0 absolute",
       button : "w-1/2 relative z-[1] text-blue-900  text-[1.1rem] py-[.1rem] border-r-[0.1rem] border-blue-900",
       selectionOptionDiv : `w-[20rem] h-[3rem] relative shrink-0 flex flex-col items-center justify-center 
       overflow-visible`,
       selectedFile : "text-[1.2rem] text-blue-900",
       rollDownContainer : "absolute bg-gray-100 w-full z-[15] top-[100%] left-0 flex overflow-x-hidden overflow-y-auto fileselector overscroll-contain shrink-0 flex-col items-start justify-start",
       containerToBeSelected : " w-full h-fit py-[.5rem] hover:bg-slate-200 text-[1.2rem] shrink-0 border-b-[0.1rem] border-b-slate-200 fileButtons flex items-center justify-between px-[1rem]",
       rollDownSvg : {selector : "down" , width : "w-[2rem]" , color : "#1E3A8A"},
       form:{input : " outline-none w-full text-blue-900 styledTextInputs text-[1.1rem] border-b-[0.1rem] border-blue-900 bg-transparent",
       label : "absolute text-[1rem]",
       selectLabel : "flex rounded-md w-full items-center justify-center py-[.2rem] shrink-0 border-[0.1rem] border-blue-900",
       button : "w-[30%] h-[2rem] flex items-center justify-center border-[0.1rem] bg-blue-900 text-white border-blue-900 py-[0.2rem]"
      }
      }
     },
     calculation : {
        readOnlyInputs : "text-[1.5rem] font-bold text-blue-900 text-start w-full border-b-[0.15rem] border-blue-900",
      parent : "w-full h-fit shrink-0 flex border-b-[0.1rem] border-slate-200 justify-evenly py-[4rem] changebg",
      subParent : "w-[60%] border-r-[0.1rem] border-slate-200 px-[3rem] h-fit flex-col justify-between flex",
      rangeParent : "flex items-start justify-start flex-col",
      rangeInput : "styledRange w-full",
      floatInput : " outline-none ULInput bg-transparent  text-[1.5rem] shrink-0 border-b-[0.15rem] duration-300 ease-in-out border-blue-900",
      submitButton : "text-[1.2rem] outline-none flex items-center justify-center hover:bg-blue-900 hover:text-white ease-in-out duration-100 text-blue-900 border-[0.1rem] h-[2.4rem] rounded-md w-[8rem] border-blue-900",
      value : "text-[1.9rem] text-blue-900 font-bold"
     },
     chartSelection : {
      parent : " w-full flex items-start justify-between border-b-[0.15rem] border-slate-200 changebg",
      chartSelectorContainer : {
       parent : "bg-slate-100 w-[30%] flex flex-col items-center justify-center ml-[.7rem] mt-[.7rem] pt-[.7rem]",
       button : {selected : "bg-gradient-to-l from-blue-200 to-blue-100 w-full py-[1.2rem] border-b-[0.1rem] border-blue-900 pl-[.7rem] flex items-center justify-start" , notSelected : "hover:bg-gradient-to-l from-transparent to-blue-200 w-full py-[1.2rem] border-b-[0.1rem] border-blue-900 pl-[.7rem] flex items-center justify-start"},
       span : "text-[1.1rem] text-blue-900 font-semibold",
       form : {
        select : "bg-transparent text-[1.1rem] w-[8rem] outline-none border-b-[.1rem] border-blue-900",
        label : " m-0"
       },
       timeTakers : {
        inputs : "outline-none bg-transparent text-[1.3rem] px-[.5rem] text-blue-900",
        heading : " text-[1.1rem] bg-white items-center absolute px-[.5rem] top-[-0.9rem] left-[1rem]  flex text-slate-400 "
       }
      }
     },
     financialAnalysis : {
        masterStyle : " w-full h-fit py-[2rem] shrink-0 flex flex-col items-center gap-[4rem] justify-start bg-white",
        formSelectorParent :" w-[25%] bg-slate-100 pt-[1rem] ml-[2rem] shrink-0 flex flex-col items-center",
        containerHeading : "text-[1.3rem] w-full bg-slate-100 py-[.5rem] text-slate-400 font-semibold",
        formOptions : {selected : "w-full border-b-[0.05rem] border-blue-900 flex items-center  bg-slate-200 justify-between" , notSelected : "w-full border-b-[0.05rem] border-blue-900 bg-slate-100 flex items-center  hover:bg-slate-200 justify-between"},
        svgEyeColor : {selected : "#1E3A8A" , notSelected : "#9CA3AF"},
        svgEyeCrossButton : "#1E3A8A",
        calculateButton  :" w-full h-[3rem] flex items-center justify-center shrink-0 mt-[2rem] text-[1.4rem] text-blue-900 border-[0.1rem] border-blue-900 rounded-full",
        formRender : {
            value : "text-[1.8rem] font-bold text-blue-900"
        },
        renderedForm : {
            headingSpan : "text-[1.3rem] white whitespace-nowrap bg-white items-center absolute px-[.5rem] top-[-1.2rem] left-[50%] translate-x-[-50%]  flex text-slate-400",
            monthsLabel : " flex-1 font-semibold text-start text-blue-900 text-[1.2rem]",
            DrInputs : "ULInput w-[25%] shrink-0 text-center outline-none",
            totalDrPaymentSpan : "flex-1"
        }
        
     }
    },
    dark : {
        toolTip : {left : "TT bg-[rgba(0,0,0,0.8)] py-[0.15rem] rounded-md border-[0.2rem] border-gray-400 px-[1rem] TTL" , middle : "TT bg-[rgba(0,0,0,0.6)] py-[0.15rem] rounded-md border-[0.2rem] border-gray-400 px-[1rem]"},
     navbar : {
      container : "w-full bg-gray-900 h-fit shrink-0 flex sticky top-0 z-[300] items-center justify-between px-[3rem] py-[1.2rem]",
      text : "text-[1.7rem] selectNone font-semibold text-white",
      svg : {selector : "sun" , width : "w-[2.4rem]" , color : "white" },
     },
     introSection : {
      parent : "w-full introSection h-fit flex bg-slate-600 flex-col",
      heading : "text-[2rem] selectNone text-start text-white font-semibold",
      fileSelectorPack :{
       toggleContainer : "w-full relative overflow-hidden h-fit shrink-0 flex border-[0.1rem] border-slate-500 rounded-xl",
       toggleBg : " w-1/2 bg-slate-500 z-[0] h-full top-0 absolute",
       button : "w-1/2 relative z-[1] text-white  text-[1.1rem] py-[.1rem] border-r-[0.1rem] border-slate-500",
       selectionOptionDiv : `w-[20rem] h-[3rem] relative shrink-0 flex flex-col items-center justify-center 
       overflow-visible`,
       selectedFile : "text-[1.2rem] text-white",
       selectedFileContainer  :" w-full border-b-[0.1rem] pb-[.5rem] border-white shrink-0 px-[1rem] gap-[1rem] flex items-center justify-between",
       rollDownContainer : "absolute fileselectorDark bg-slate-600 w-full z-[15] top-[100%] left-0 flex overflow-x-hidden overflow-y-auto overscroll-contain shrink-0 flex-col items-start justify-start",
       containerToBeSelected : " text-white py-[0.5rem] text-[1.2rem] w-full h-fit hover:bg-slate-500 shrink-0 border-b-[0.1rem] fileButtons border-b-slate-200 flex items-center justify-between px-[1rem]",
       rollDownSvg : {selector : "down" , width : "w-[2rem]" , color : "white"},
       form:{input : " outline-none w-full text-white styledTextInputs text-[1.1rem] border-b-[0.1rem] border-white bg-transparent",
       label : "absolute text-[1rem] text-white",
       selectLabel : "flex rounded-md w-full items-center justify-center text-white py-[.2rem] shrink-0 border-[0.1rem] border-white",
       button : "w-[30%] flex items-center justify-center border-[0.1rem] bg-slate-500 text-white border-slate-500 py-[0.2rem]"
      }
      }
     },
     calculation : {
    readOnlyInputs : "text-[1.5rem] font-bold text-gray-400 text-start w-full border-b-[0.15rem] border-gray-400",
      parent : "w-full h-fit shrink-0 flex border-b-[0.1rem] bg-gray-900 border-slate-200 justify-evenly py-[4rem]",
      subParent : "w-[60%] border-r-[0.1rem] border-slate-200 px-[3rem] h-fit flex-col justify-between flex",
      rangeParent : "flex items-start justify-start flex-col text-white",
      rangeInput : "styledRangeDark w-full",
      floatInput : " outline-none bg-transparent text-white text-[1.5rem] shrink-0 border-b-[0.15rem] duration-300 ease-in-out border-white",
      submitButton : "text-[1.2rem] outline-none flex items-center justify-center hover:bg-gray-700 hover:text-white ease-in-out duration-100 text-white border-[0.1rem] h-[2.4rem] rounded-md w-[8rem] border-white",
      value : "text-[1.9rem] text-white font-bold"
     },
     chartSelection : {
      parent : " w-full flex items-start justify-between bg-gray-900 border-b-[0.15rem] border-slate-200",
      chartSelectorContainer : {
       parent : "bg-gray-700 w-[30%] flex flex-col items-center justify-center ml-[.7rem] mt-[.7rem] pt-[.7rem]",
       button : {selected : "bg-gray-600 w-full py-[1.2rem] border-b-[0.1rem] border-gray-400 pl-[.7rem] flex items-center justify-start" , notSelected : "hover:bg-gray-600 w-full py-[1.2rem] border-b-[0.1rem] border-gray-400 pl-[.7rem] flex items-center justify-start"},
       span : "text-[1.1rem] text-gray-400 font-semibold",
       form : {
        select : "bg-gray-900 text-white text-[1.1rem] w-[8rem] outline-none border-b-[.1rem] border-white",
        label : " m-0 text-white"
       },
       timeTakers : {
        inputs : "outline-none darkDateInput bg-transparent text-[1.3rem] px-[.5rem] text-white",
        heading : " text-[1.1rem] bg-gray-900 items-center absolute px-[.5rem] top-[-0.9rem] left-[1rem]  flex text-slate-400 "
       }
      }
     },
     financialAnalysis : {
        masterStyle : " w-full h-fit py-[2rem] shrink-0 flex flex-col items-center gap-[4rem] justify-start bg-gray-900",
        formSelectorParent :" w-[25%]  bg-gray-600 pt-[1rem] ml-[2rem] shrink-0 flex flex-col items-center",
        containerHeading : "text-[1.3rem] w-full bg-gray-700 py-[.5rem] text-white font-semibold",
        formOptions : {selected : "w-full border-b-[0.05rem] border-gray-400 flex items-center  bg-slate-600 text-gray-400 justify-between" , notSelected : "w-full border-b-[0.05rem] border-slate-400 bg-gray-700 text-gray-400 flex items-center  hover:bg-slate-600 justify-between"},
        svgEyeColor : {selected : "white" , notSelected : "#9CA3AF"},
        svgEyeCrossButton : "white",
        calculateButton  :" w-full h-[3rem] flex items-center justify-center shrink-0 mt-[2rem] text-[1.4rem] text-white border-[0.1rem] border-white rounded-full",
        formRender : {
            value : "text-[1.8rem] font-bold text-white"
        },
        renderedForm : {
            headingSpan : "text-[1.3rem] whitespace-nowrap bg-gray-900 items-center absolute px-[.5rem] top-[-1.2rem] left-[50%] translate-x-[-50%]  flex text-slate-400",
            monthsLabel : " flex-1 font-semibold text-start text-gray-400 text-[1.2rem]",
            DrInputs : "ULInput w-[25%] shrink-0 text-center outline-none bg-transparent text-white",
            totalDrPaymentSpan : "flex-1 text-white"
        }
     }
    }
   }