const BASE_URL = "http://localhost:8000";

export async function getTodaySessions() {
  const res = await fetch(`${BASE_URL}/sessions/today`);
  return await res.json();
}


export async function getDailyReport(date) {
  let url = "http://localhost:8000/reports/daily";
  if (date) {
    url += `?date=${date}`;
  }
  const res = await fetch(url);
  return await res.json();
}
