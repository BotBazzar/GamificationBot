import { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { HashRouter as Router, Routes, Route } from "react-router-dom";
import Interface from "./interface/Interface";
import Game from "./Game";
import Leaderboard from "./Leaderboard";

const App = () => {
  const [windowWidth] = useState(window.innerWidth);
  const cameraPositionZ = windowWidth > 500 ? 30 : 40;
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Interface />
              <Canvas camera={{ fov: 75, position: [0, 0, cameraPositionZ] }}>
                <Game />
              </Canvas>
            </>
          }
        />

        <Route
          path="/leaderboard"
          element={
            <Leaderboard
              users={[
                { name: "Player 1", score: 1000 },
                { name: "Player 2", score: 850 },
                { name: "Player 3", score: 700 },
              ]}
            />
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
