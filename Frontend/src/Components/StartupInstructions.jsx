import React, { useContext } from "react";
import { stylings } from "../UTILS/UTILS_STYLES";
import { globalContext } from "../Context/Context";
import { FaHandPointUp, FaRunning, FaEye } from "react-icons/fa";
import { LuSettings2 } from "react-icons/lu";

const StartupInstructions = ({ onHover, onHoverOut }) => {
  const { theme } = useContext(globalContext);
  const style = stylings[theme].startupInstructions;

  return (
    <div
      className={style.mainDiv}
      onMouseEnter={onHover}
      onMouseLeave={onHoverOut}
    >
      <div className={style.gridLayout}>
        {[1, 2, 3, 4].map((item) => (
          <div
            key={item}
            className={`${style.gridItem} ${item !== 4 ? "border-r-2" : ""} `}
          >
            <div className={style.itemTitle}>{item}</div>
            <div className={style.itemDesc + " font-semibold"}>
              {item === 1 && (
                <div className="flex flex-col items-center gap-2">
                  Select a Building for Analysis or upload your own load
                  profile.
                  <FaHandPointUp size={50} />
                </div>
              )}
              {item === 2 && (
                <div className="flex flex-col items-center gap-2">
                Adjust BESS inputs if necessary, then click Submit.
                <LuSettings2 size={50} />
                </div>
              )}
              {item === 3 && (
                <div className="flex flex-col items-center gap-2">
                  Run financial analysis, demand forecasting, and load profile
                  models
                  <FaRunning size={50} />
                </div>
              )}
              {item === 4 && (
                <div className="flex flex-col items-center gap-2">
                  Review the outputs and analyze your results.
                  <FaEye size={50}/>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StartupInstructions;
