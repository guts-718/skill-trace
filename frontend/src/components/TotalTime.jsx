export default function TotalTime({ sessions }) {
  const totalSec = sessions.reduce(
    (sum, s) => sum + s.duration_sec,
    0
  );

  const minutes = Math.floor(totalSec / 60);
  const seconds = totalSec % 60;

  return (
    <h3>
      Total Today: {minutes} min {seconds} sec
    </h3>
  );
}
