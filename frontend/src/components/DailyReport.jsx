export default function DailyReport({ report }) {
  if (!report) return null;

  if (report.error === "future") {
    return <p>🧭 You haven't lived that day yet.</p>;
  }

  if (report.error === "nodata") {
    return (
      <p>
        📭 No records for this day.
        We weren’t a thing yet.
      </p>
    );
  }

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>Daily Report: {report.date}</h3>

      <p>Total Time: {Math.floor(report.total_time_sec / 60)} minutes</p>
      <p>Sessions: {report.session_count}</p>

      <h4>Category Breakdown</h4>
      <ul>
        {Object.entries(report.category_breakdown).map(
          ([cat, time]) => (
            <li key={cat}>
              {cat}: {Math.floor(time / 60)} min
            </li>
          )
        )}
      </ul>

      <h4>Top Domains</h4>
      <ul>
        {report.top_domains.map((d, i) => (
          <li key={i}>
            {d.domain}: {Math.floor(d.time / 60)} min
          </li>
        ))}
      </ul>
    </div>
  );
}
