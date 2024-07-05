import React from 'react'
import { insertCommas } from '../../UTILS/UTILS_HELPERS'
import { stylings } from '../../UTILS/UTILS_STYLES'
import { globalContext } from '../../Context/Context'
import ToolTip from '../NumbersData/ToolTip'

export default function Results({results , renderResultsHelper}) {
  const {theme} = React.useContext(globalContext)
 const amtInDollars = ["npv" , "itc" , "year1_bill_savings" , "dr_capacity_revenue" ]
  return (
    <div className='div w-[40%] flex items-center gap-[.5rem] justify-between flex-wrap'>
     {renderResultsHelper.map((val , index) =>
     {
      return<div className={`${index === 0 ? "w-[100%]" : "w-[48%]"} p-[0.7em] shrink-0 flex flex-col items-center`}>
       {/* <div className=" flex flex-col items-start"> */}
       <span className=' text-[1.3rem] text-slate-400'><label className='relative'>{val.label}
       <ToolTip text={val.tooltip} left={true}/>
       </label></span>
       <span className={stylings[theme].financialAnalysis.formRender.value}>{amtInDollars.includes(val.accessor) ? `$${insertCommas(results[val.accessor])}` : results[val.accessor]}{val.backLabel ? <span className=' text-[0.9rem] text-slate-400 font-normal'>{val.backLabel}</span> : ""}</span>
       {/* </div> */}
      </div>
     })}
    </div>
  )
}
  