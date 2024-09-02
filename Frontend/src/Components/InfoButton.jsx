import React, { useState, useEffect, useRef } from "react";
import { IoMdInformationCircleOutline } from "react-icons/io";

const InfoButton = () => {
  const [showTooltip, setShowTooltip] = useState(false);
  const buttonRef = useRef(null);
  const tooltipRef = useRef(null);

  const handleClickOutside = (event) => {
    if (
      tooltipRef.current && 
      !tooltipRef.current.contains(event.target) &&
      buttonRef.current &&
      !buttonRef.current.contains(event.target)
    ) {
      setShowTooltip(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div>
      <div
         ref={buttonRef}
        className="absolute -top-2 right-3 hover:cursor-pointer"
        onClick={() => setShowTooltip(!showTooltip)}
      >
        <IoMdInformationCircleOutline size={20} />
      </div>
      {showTooltip && (
        <div
          ref={tooltipRef}
          className="absolute top-3 right-0 mt-2 w-1/2 bg-white shadow-lg rounded-lg p-4 border border-gray-200 z-10"
        >
          <p className="text-sm text-gray-700 mb-2">
            You can download our sample sheet to get a better understanding of the data structure.
          </p>
          <a
            href="/Administration Building.xlsx"
            download
            className="text-blue-500 font-bold hover:underline inline-block"
            onClick={() => setShowTooltip(false)} 
          >
            Download
          </a>
        </div>
      )}
    </div>
  );
};

export default InfoButton;
