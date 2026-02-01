let lastUrl = null;
const BACKEND_URL = "http://localhost:8000/event";

function sendEvent(tab) {
  if (!tab || !tab.url) return;

  if (tab.url === lastUrl) return;

  const payload = {
    url: tab.url,
    title: tab.title || "",
    domain: new URL(tab.url).hostname,
    referrer: lastUrl,
    timestamp: Math.floor(Date.now() / 1000)
  };

  lastUrl = tab.url;

  console.log("Sending event:", payload);

  fetch(BACKEND_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  }).catch((e) => {
    console.warn("Error ", e);
  });
}


// When user switches tab
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  const tab = await chrome.tabs.get(activeInfo.tabId);
  sendEvent(tab);
});

// When tab URL changes
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete") {
    sendEvent(tab);
  }
});

// When window gains focus
chrome.windows.onFocusChanged.addListener(async (windowId) => {
  if (windowId === chrome.windows.WINDOW_ID_NONE) return;

  const tabs = await chrome.tabs.query({
    active: true,
    windowId: windowId
  });

  if (tabs.length > 0) {
    sendEvent(tabs[0]);
  }
});
