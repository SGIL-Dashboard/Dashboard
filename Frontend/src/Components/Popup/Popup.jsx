import React from "react";
import "./Popup.scss";
import SVGComponent from "../SVGS/SVGS";
export default function Popup({ children, onClose }) {
  return (
    <div className=" w-[100vw] z-[400] h-[100vh] fixed top-0 left-0 popupMaster">
      <div className="w-full h-full">
        <button onClick={onClose} className=" absolute top-3 z-[1] right-3">
          <SVGComponent selector={"cross"} width={"w-[1rem]"} color="white" />
        </button>
        <div
          onClick={onClose}
          className=" shrink-0 absolute top-0 left-0 w-full h-full"
        ></div>
        {children}
      </div>
    </div>
  );
}
