let aliveSecond = 0;
let heartBeatRate = 5000;
let pubnub;
let appChannel = "johns-pi";

// Timer variables
let timerSeconds = 900; // 15 minutes in seconds
let timerInterval = null;
let isRunning = false;

function time() {
  let d = new Date();
  let currentSecond = d.getTime();
  if (currentSecond - aliveSecond > heartBeatRate + 1000) {
    document.getElementById("connection_id").innerHTML = "DEAD";
  } else {
    document.getElementById("connection_id").innerHTML = "ALIVE";
  }
  setTimeout("time()", 1000);
}

function keepAlive() {
  fetch("/keep_alive")
    .then((response) => {
      if (response.ok) {
        let date = new Date();
        aliveSecond = date.getTime();
        return response.json();
      }
      throw new Error("Server offline");
    })
    .catch((error) => console.log(error));
  setTimeout("keepAlive", heartBeatRate);
}

function handleClick(cb) {
  if (cb.checked) {
    value = "on";
  } else {
    value = "off";
  }
  publishMessage({ buzzer: value });
}

const setupPubNub = () => {
  pubnub = new pubnub({
    publishKey: "your_publish_key",
    subscribeKey: "your_subscribe_key",
    userId: "johns_laptop",
  });

  //create a channel
  const channel = pubnub.channel(appChannel);
  //create a subscription
  const subscription = channel.subscription();

  pubnub.addListener({
    status: (s) => {
      console.log("Status", s.category);
    },
  });

  subscription.onMessage = (messageEvent) => {
    handleMessage(messageEvent.message);
  };
  subscription.subscribe();
};

// Timer functions
function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function updateTimerDisplay() {
  const timerElement = document.getElementById('timer');
  if (timerElement) {
    timerElement.textContent = formatTime(timerSeconds);
  }
}

function toggleTimer() {
  const btn = document.getElementById('startStopBtn');
  
  if (isRunning) {
    // Stop the timer
    clearInterval(timerInterval);
    timerInterval = null;
    isRunning = false;
    btn.textContent = '▶ Start';
  } else {
    // Start the timer
    isRunning = true;
    btn.textContent = '⏸ Stop';
    
    timerInterval = setInterval(() => {
      if (timerSeconds > 0) {
        timerSeconds--;
        updateTimerDisplay();
      } else {
        // Timer finished
        clearInterval(timerInterval);
        timerInterval = null;
        isRunning = false;
        btn.textContent = '▶ Start';
        alert('Timer finished!');
      }
    }, 1000);
  }
}

function adjustTime(minutes) {
  timerSeconds += minutes * 60;
  if (timerSeconds < 0) {
    timerSeconds = 0;
  }
  updateTimerDisplay();
}

function saveCookingSession() {
  // TODO: Add database save logic here
  alert('Cooking session saved!');
  console.log('Session data to save:', {
    timeRemaining: timerSeconds,
    formattedTime: formatTime(timerSeconds),
    timestamp: new Date().toISOString()
  });
}
