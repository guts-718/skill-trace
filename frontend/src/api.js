const BASE_URL = "http://localhost:8000";

export async function getTodaySessions() {
  const res = await fetch(`${BASE_URL}/sessions/today`);
  return await res.json();
}
