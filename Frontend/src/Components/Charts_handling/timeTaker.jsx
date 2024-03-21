import React from 'react'

export default function TimeTaker({current , comparision , lessThan , timeSelection , setTimeSelection , label}) {
const noErrors = (new Date(timeSelection.from) < new Date(timeSelection.to));
 console.log({vvv : new Date(timeSelection.from) > new Date(timeSelection.to)})
  return (
   <div className={!noErrors ? "div relative w-[17rem] h-[6.3rem] rounded-xl justify-center shrink-0 flex flex-col border-[0.15rem] border-red-500" : "div relative w-[17rem] h-[6.3rem] rounded-xl justify-center shrink-0 flex flex-col border-[0.15rem] border-slate-400"}>
   <span className=' text-[1.1rem] bg-white items-center absolute px-[.5rem] top-[-0.9rem] left-[1rem]  flex text-slate-400 '>{label}</span>
   <input value={timeSelection[current].split("T")[0]} onChange={(e)=>
     {
      setTimeSelection({...timeSelection ,[current] : e.target.value + "T" + timeSelection[current].split("T")[1]})
       console.log({val : e.target.value})
     }} type="date"  className=' outline-none text-[1.3rem] px-[.5rem] text-blue-900'/>
   <input value={timeSelection[current].split("T")[1]} onChange={(e)=>
     {
      setTimeSelection({...timeSelection ,[current] : timeSelection[current].split("T")[0] + "T" + e.target.value})
       console.log({val : e.target.value})
     }} type="time"  className=' outline-none text-[1.3rem] px-[.5rem] text-blue-900'/>
 </div>
  )
}
