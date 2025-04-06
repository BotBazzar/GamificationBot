import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useTelegram } from "./providers/TelegramProvider";

interface LeaderboardProps {
  users: Array<{ first_name: string; last_name: string; username: string; score: number }>;
}

const Leaderboard: React.FC<LeaderboardProps> = ({ users }) => {
  const [leaderboard, setLeaderboard] = useState(users);
  const { user } = useTelegram();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      //https://api.botbazaar.ir
      try {
        const res = await fetch(`http://localhost:8000/app/leaderboard/`);
        if (!res.ok) {
          throw new Error("خطا در دریافت رتبه‌بندی");
        }
        const data = await res.json();
        setLeaderboard(data);
        console.log("Leaderboard data:", data);
        // Update the leaderboard state with the fetched data
      } catch (err) {
        console.error("Error fetching leaderboard:", err);
        setError("خطا در دریافت رتبه‌بندی. لطفاً دوباره تلاش کنید.");
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {
    return (
      <div className="leaderboard-container" dir="rtl">
        <h2 style={{ textAlign: "center", fontSize: "24px", color: "#6c757d" }}>
          {user?.first_name} {user?.last_name} خوش آمدید
        </h2>
        <div className="loading-spinner"></div>
        <p style={{ marginTop: "10px", fontSize: "16px", color: "#6c757d" }}>
          در حال بارگذاری رتبه‌بندی...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="leaderboard-container" dir="rtl">
        <p style={{ color: "#dc3545", textAlign: "center", marginTop: "20px" }}>
          {error}
        </p>
        <button
          className="refresh-button"
          onClick={() => window.location.reload()}
        >
          🔄 بروزرسانی
        </button>
      </div>
    );
  }

  return (
    <div className="leaderboard-container" dir="rtl">
      <h1 style={{ textAlign: "center", color: "#2c3e50" }}>🏆 رتبه‌بندی</h1>

      <div className="leaderboard-content">
        <table className="leaderboard-table">
          <thead>
            <tr>
              <th>رتبه</th>
              <th>نام کاربری</th>
              <th>امتیاز</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((u, index) => (
              <tr
                key={index}
                className={
                  index === 0
                    ? "first-place"
                    : index === 1
                    ? "second-place"
                    : index === 2
                    ? "third-place"
                    : ""
                }
              >
                <td>{index + 1}</td>
                <td>{u?.username}</td>
                <td>{u?.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="leaderboard-footer">
        <p style={{ color: "#6c757d", textAlign: "center", marginTop: "20px" }}>
          به روزرسانی:{" "}
          {new Date().toLocaleDateString("fa-IR", {
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
        </p>
      </div>
      <Link to="/" className="back-button">
        بازگشت به بازی
      </Link>
    </div>
  );
};

export default Leaderboard;
