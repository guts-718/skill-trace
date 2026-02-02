import { useEffect, useState } from "react";
import { getTodaySessions } from "./api";
import TotalTime from "./components/TotalTime";
import SessionTable from "./components/SessionTable";
import { getDailyReport } from "./api";
import DailyReport from "./components/DailyReport";
import Settings from "./components/Settings";


function App() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);

  const [report, setReport] = useState(null);
  const [reportDate, setReportDate] = useState("");


  async function loadSessions() {
    setLoading(true);
    const data = await getTodaySessions();
    setSessions(data);
    setLoading(false);
  }

  async function loadReport() {
    if (reportDate) {
      const selected = new Date(reportDate);
      const today = new Date();

      if (selected > today) {
        setReport({
          error: "future"
        });
        return;
      }
    }

    const data = await getDailyReport(reportDate);

    if (data.session_count === 0) {
      setReport({
        error: "nodata",
        date: reportDate
      });
      return;
    }

    setReport(data);
  }



  async function overrideCategory(id) {
  const cat = prompt("Enter new category");
  if (!cat) return;

  await fetch(`http://localhost:8000/sessions/${id}/override`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ category: cat })
  });

  loadSessions();
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
      <div style={{ marginTop: "20px" }}>
        <input
          type="date"
          value={reportDate}
          onChange={(e) => setReportDate(e.target.value)}
        />

        <button onClick={loadReport}>
          Load Report
        </button>
      </div>

      <DailyReport report={report} />

      <Settings />

      {loading && <p>Loading...</p>}

      <TotalTime sessions={sessions} />

      <SessionTable sessions={sessions} onOverride={overrideCategory} />
    </div>
  );
}

export default App;
