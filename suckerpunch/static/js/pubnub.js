async function initPubNub() {
  try {
    // Initialize PubNub WITHOUT fetching a token
    const pubnub = new PubNub({
      subscribeKey: PUBNUB_SUB_KEY, 
      uuid: "web-client",
    });

    console.log("PubNub initialized without token (Access Manager disabled)");

    pubnub.subscribe({
      channels: ["suckerpunch.motion"],
    });

    pubnub.addListener({
      message: function(event) {
        console.log("New punch event received:", event.message);
        
        if (typeof incrementCounter === 'function') {
          incrementCounter();
        }
      },
      status: function(event) {
        if (event.category === "PNConnectedCategory") {
          console.log("PubNub subscribed and ready");
        }
      }
    });

    // Make pubnub instance available globally
    window.pubnub = pubnub;

  } catch (error) {
    console.error("Error initializing PubNub:", error);
  }
}

// Helper function to update a log on the page
function updatePunchLog(msg) {
  const logElement = document.getElementById('punch-log');
  if (logElement) {
    const entry = document.createElement('div');
    const time = msg.human_time ? new Date(msg.human_time).toLocaleTimeString() 
                : new Date(msg.timestamp * 1000).toLocaleTimeString();
    entry.textContent = `Punch at ${time} (Device: ${msg.device_id || 'Unknown'})`;
    logElement.prepend(entry);
  }
}
document.addEventListener('DOMContentLoaded', initPubNub);