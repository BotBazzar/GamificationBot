// PrizeWheel.tsx

import React, { useState } from "react";
import { Wheel } from "react-custom-roulette";
import { Prize } from "./types";

interface PrizeWheelProps {
  data: { option: string }[];
  prizeIndex: number;
  onSpinComplete: () => void;
}

const PrizeWheel: React.FC<PrizeWheelProps> = ({
  data,
  prizeIndex,
  onSpinComplete,
}) => {
  const [mustSpin, setMustSpin] = useState(false);

  const handleSpinClick = () => {
    setMustSpin(true);
  };

  return (
    <div className="prize-wheel-container">
      <Wheel
        mustStartSpinning={mustSpin}
        prizeNumber={prizeIndex}
        data={data}
        backgroundColors={[
          "#3e3e3e",
          "#df3428",
          "#2c3e50",
          "#e74c3c"
        ]}
        textColors={[
          "#ffffff",
          "#000000"
        ]}
        fontSize={20}
        fontFamily={"Vazirmatn, sans-serif"}
        textDistance={100}
        onStopSpinning={() => {
          setMustSpin(false);
          onSpinComplete();
        }}
      />

      {!mustSpin && (
        <button
          onClick={handleSpinClick}
          style={{
            marginTop: "30px",
            width: "100%",
            padding: "3px 20px",
            fontSize: "22px",
            borderRadius: "15px",
            backgroundColor: "#2ecc71",
            color: "white",
            border: "none",
            cursor: "pointer",
            boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
            transition: "all 0.3s ease",
            fontFamily: "Vazirmatn, sans-serif"
          }}
        >
          🎲 چرخاندن!
        </button>
      )}
    </div>
  );
};

export default PrizeWheel;
