import { useState } from "react";
import { Link } from "react-router-dom";
import { useTelegram } from "./providers/TelegramProvider";

interface LeaderboardProps {
  users: Array<{ name: string; score: number }>;
}

const Leaderboard: React.FC<LeaderboardProps> = ({ users }) => {
  const [leaderboard] = useState(users);
  const { webApp, user } = useTelegram();
  return (
    <div className="leaderboard-container">
      {user && (
        <h2 style={{ textAlign: "center", fontSize: "24px", color: "#6c757d" }}>
          {user.first_name} {user.last_name} خوش آمدید
        </h2>
      )}
      <h1>Leaderboard</h1>
      <div className="leaderboard-content">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Name</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((user, index) => (
              <tr key={user.name}>
                <td>{index + 1}</td>
                <td>{user.name}</td>
                <td>{user.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Link to="/" className="back-button">
        Back to Game
      </Link>
    </div>
  );
};

export default Leaderboard;
