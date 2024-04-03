import React from 'react'
import { insertCommas } from '../../UTILS/UTILS_HELPERS'

export default function Results({results , renderResultsHelper}) {
 const amtInDollars = ["npv" , "itc" , "bill_savings_yr1" , "dr_rev_yr1" ]
  return (
    <div className='div w-[40%] flex items-center gap-[.5rem] justify-between flex-wrap'>
     {renderResultsHelper.map((val , index) =>
     {
      return<div className={`${index === 0 ? "w-[100%]" : "w-[48%]"} p-[0.7em] shrink-0 flex flex-col items-center`}>
       {/* <div className=" flex flex-col items-start"> */}
       <span className=' text-[1.3rem] text-slate-400'>{val.label}</span>
       <span className=' text-[1.8rem] font-bold text-blue-900'>{amtInDollars.includes(val.accessor) ? `$${insertCommas(results[val.accessor])}` : results[val.accessor]}{val.backLabel ? <span className=' text-[0.9rem] text-slate-400 font-normal'>{val.backLabel}</span> : ""}</span>
       {/* </div> */}
      </div>
     })}
    </div>
  )
}
  