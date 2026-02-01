export default function SessionTable({ sessions }) {
  return (
    <table border="1" cellPadding="8">
      <thead>
        <tr>
          <th>Start</th>
          <th>End</th>
          <th>Duration (sec)</th>
          <th>Category</th>
          <th>Title</th>
          <th>Domain</th>
        </tr>
      </thead>

      <tbody>
        {sessions.map((s, idx) => (
          <tr key={idx}>
            <td>{new Date(s.start_time * 1000).toLocaleTimeString()}</td>
            <td>{new Date(s.end_time * 1000).toLocaleTimeString()}</td>
            <td>{s.duration_sec}</td>
            <td style={{ fontWeight: "bold" }}>{s.category}</td>
            <td>{s.title}</td>
            <td>{s.domain}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
