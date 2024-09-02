import React from "react";
import { globalContext } from "../../Context/Context";
import { stylings } from "../../UTILS/UTILS_STYLES";
export default function ToolTip({ text, left }) {
  const { theme } = React.useContext(globalContext);
  return (
    <div
      className={
        left ? stylings[theme].toolTip.left : stylings[theme].toolTip.middle
      }
    >
      <span className=" font-bold text-white">{text}</span>
    </div>
  );
}
