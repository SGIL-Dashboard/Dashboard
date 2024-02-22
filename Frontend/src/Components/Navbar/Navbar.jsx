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
     <div className="flex shrink-0 items-center justify-center gap-[.5rem]">
      <img src={assets.logo} alt="img" className=' w-[3rem]'/>
     <span style={{ fontFamily: 'Source Sans Pro' }} className={stylings[theme].navbar.text}>{navbarContent.companyName}</span>
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
