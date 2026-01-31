import { useEffect, useState } from "react";
import { getTodaySessions } from "./api";
import TotalTime from "./components/TotalTime";
import SessionTable from "./components/SessionTable";


function App() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);

  async function loadSessions() {
    setLoading(true);
    const data = await getTodaySessions();
    setSessions(data);
    setLoading(false);
  }

  useEffect(() => {
    loadSessions();

    const interval = setInterval(() => {
      loadSessions();
    }, 120000); // 2 minutes

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>SkillTrace - Today's Activity</h2>

      <button onClick={loadSessions}>Refresh</button>

      {loading && <p>Loading...</p>}

      <TotalTime sessions={sessions} />

      <SessionTable sessions={sessions} />
    </div>
  );
}

export default App;
