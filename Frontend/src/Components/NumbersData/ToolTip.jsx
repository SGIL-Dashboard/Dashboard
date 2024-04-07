import React from 'react'

export default function ToolTip({text}) {
  return (
    <div className='TT bg-[rgba(30,64,175,0.8)] py-[0.15rem] rounded-md border-[0.2rem] border-blue-400 px-[1rem]'>
     <span className=' whitespace-nowrap text-white'>{text}</span>
    </div>
  )
}
