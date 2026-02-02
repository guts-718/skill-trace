import { useEffect, useState } from "react";
import { getSettings, saveSettings } from "../api";

export default function Settings() {
  const [settings, setSettings] = useState(null);

  useEffect(() => {
    getSettings().then(setSettings);
  }, []);

  if (!settings) return <p>Loading settings...</p>;

  function update(key, value) {
    setSettings({ ...settings, [key]: value });
  }

  async function handleSave() {
    await saveSettings(settings);
    alert("Settings saved");
  }

  return (
    <div style={{ marginTop: "30px" }}>
      <h3>Settings</h3>

      <div>
        <label>Daily Report Time:</label><br />
        <input
          type="time"
          value={settings.report_time}
          onChange={(e) => update("report_time", e.target.value)}
        />
      </div>

      <br />

      <div>
        <label>Email:</label><br />
        <input
          type="email"
          value={settings.email}
          onChange={(e) => update("email", e.target.value)}
        />
      </div>

      <div>
        <input
          type="checkbox"
          checked={settings.enable_email}
          onChange={(e) => update("enable_email", e.target.checked)}
        />
        Enable Email Reports
      </div>

      <br />

      <div>
        <label>Telegram:</label><br />
        {settings.telegram_chat_id
          ? "Connected ✅"
          : "Not connected. Open bot and send /start"}
      </div>

      <div>
        <input
          type="checkbox"
          checked={settings.enable_telegram}
          onChange={(e) => update("enable_telegram", e.target.checked)}
        />
        Enable Telegram Reports
      </div>

      <br />

      <button onClick={handleSave}>
        Save Settings
      </button>
    </div>
  );
}
