import React from 'react'
import { navbarContent } from './Content'
import { assets } from '../../UTILS/UTILS_Assets'
import SVGComponent from '../SVGS/SVGS'
import { globalContext } from '../../Context/Context'
import { useContext } from 'react'
import { stylings } from '../../UTILS/UTILS_STYLES'
export default function Navbar() {
  const {theme  , setTheme} = useContext(globalContext);
  return (
    <div className={stylings[theme].navbar.container}>
     <div className="flex shrink-0 items-center justify-center gap-[1rem]">
      <img src={assets.logo} alt="img" className=' w-[5rem]'/>
      <div className=" flex flex-col items-start">
     <span  className={stylings[theme].navbar.text}>Smart Grid Interdependencies Laboratory</span>
     <span  className={stylings[theme].navbar.text}>SGIL Load Analysis and Battery Sizing (LABS)</span>
      </div>
     </div>
     <button onClick={()=>
      {
        if(theme === "dark")
        {
          setTheme("light")
        }
        else
        {
          setTheme("dark")
        }
      }}><SVGComponent {...stylings[theme].navbar.svg}/></button>
    </div>
  )
}
