// WheelPage.tsx

import React, { useEffect, useState } from "react";
import PrizeWheel from "./PrizeWheel";
import { PrizeApiResponse } from "./types";
import { useTelegram } from "./providers/TelegramProvider";

const WheelPage: React.FC = () => {
  const [prizeIndex, setPrizeIndex] = useState<number | null>(null);
  const [hasSpun, setHasSpun] = useState<boolean>(false);
  const [prizeData, setPrizeData] = useState<{ option: string }[]>([]);
  const prizeImages = [
    "/images/prize_1.webp",
    "/images/prize_2.jpg",
    "/images/prize_3.jpg",
  ];
  const [loading, setLoading] = useState<boolean>(true);
  const BASE_URL = "https://api.botbazaar.ir"; // "http://localhost:8000";
  const { user } = useTelegram();

  useEffect(() => {
    if (user?.id) {
      const fetchPrize = async () => {
        try {
          const res = await fetch(
            `${BASE_URL}/app/prizes/?chat_id=${user.id}`
          );
          const data: PrizeApiResponse = await res.json();

          setPrizeIndex(data.prizeIndex);
          setHasSpun(data.hasSpun);
          setPrizeData(data.prizeList.map((prize) => ({ option: prize.name })));
        } catch (err) {
          console.error("Error fetching prize:", err);
        } finally {
          setLoading(false);
        }
      };

      fetchPrize();
    }
  }, []);

  const handleSpinComplete = async () => {
    try {
      await fetch(`${BASE_URL}/app/mark-spun/?chat_id=${user?.id}`, {
        method: "POST",
      });
      setHasSpun(true);
    } catch (err) {
      console.error("Error marking spin:", err);
    }
  };

  if (loading)
    return (
      <div style={{ textAlign: "center", padding: "20px" }}>
        <div className="loading-spinner"></div>
        <p style={{ marginTop: "10px", fontSize: "16px", color: "#6c757d" }}>
          در حال بارگذاری...
        </p>
      </div>
    );

  return (
    <div className="wheel-container" dir="rtl">
      <h2 style={{ textAlign: "center", fontSize: "24px", color: "#6c757d" }}>
        {user?.first_name} {user?.last_name} خوش آمدید
      </h2>
      <h1 className="wheel-title">🎁 گردونه شانس!</h1>

      {hasSpun ? (
        <div className="prize-card">
          <h2>شما قبلاً چرخ را چرخانده‌اید!</h2>
          <div className="prize-image-container">
            <img
              src={prizeImages[prizeIndex ?? 0]}
              alt="جایزه شما"
              className="prize-image"
            />
          </div>
          <p className="prize-description">
            برای شرکت در دور بعدی، منتظر بمانید تا فرصت بعدی شما فرا رسیده باشد.
          </p>
        </div>
      ) : (
        prizeIndex !== null && (
          <>
            <PrizeWheel
              data={prizeData}
              prizeIndex={prizeIndex}
              onSpinComplete={handleSpinComplete}
            />
          </>
        )
      )}
    </div>
  );
};

export default WheelPage;
