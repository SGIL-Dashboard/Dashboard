import React from 'react'
import { globalContext } from '../../Context/Context';
import { stylings } from '../../UTILS/UTILS_STYLES';
export default function TimeTaker({current , comparision , lessThan , timeSelection , setTimeSelection , label}) {
  const {theme} = React.useContext(globalContext);
const noErrors = (new Date(timeSelection.from) < new Date(timeSelection.to));
 console.log({vvv : new Date(timeSelection.from) > new Date(timeSelection.to)})
  return (
   <div className={!noErrors ? "div relative w-[25%] rounded-xl p-[.5rem] justify-center shrink-0 flex flex-col border-[0.15rem] border-red-500" : "div relative w-[25%] rounded-xl p-[.5rem] justify-center shrink-0 flex flex-col border-[0.15rem] border-slate-400"}>
   <span className={stylings[theme].chartSelection.chartSelectorContainer.timeTakers.heading}>{label}</span>
   <input value={timeSelection[current].split("T")[0]} onChange={(e)=>
     {
      setTimeSelection({...timeSelection ,[current] : e.target.value + "T" + timeSelection[current].split("T")[1]}) 
       console.log({val : e.target.value})
     }} type="date"  className={stylings[theme].chartSelection.chartSelectorContainer.timeTakers.inputs}/>
   <input value={timeSelection[current].split("T")[1]} onChange={(e)=>
     {
      setTimeSelection({...timeSelection ,[current] : timeSelection[current].split("T")[0] + "T" + e.target.value})
       console.log({val : e.target.value})
     }} type="time"  className={stylings[theme].chartSelection.chartSelectorContainer.timeTakers.inputs}/>
 </div>
  )
}
