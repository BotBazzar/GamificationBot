import { useState } from "react";
import { Link } from "react-router-dom";

interface LeaderboardProps {
  users: Array<{ name: string; score: number }>;
}

const Leaderboard: React.FC<LeaderboardProps> = ({ users }) => {
  const [leaderboard] = useState(users);
  return (
    <div className="leaderboard-container">
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
