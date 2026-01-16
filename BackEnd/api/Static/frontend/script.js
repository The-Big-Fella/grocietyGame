async function load_game_state() {
  const res = await fetch("/game_state");
  const data = await res.json();

  console.log(data);

  // Top level data
  let moodElements = document.querySelectorAll("#mood");
  let budgetElements = document.querySelectorAll("#budget");

  // Timer module data (nested)
  let timerElements = document.querySelectorAll("#timer");
  let penaltyElements = document.querySelectorAll("#penalty-cost");
  let remainingElements = document.querySelectorAll("#remaining-events");

  // Setting the values
  setNodeListText(moodElements, data.mood);
  setNodeListText(budgetElements, data.budget);

  if (data.timer) {
    // Time remaining (rounded to whole number for cleaner UI)
    const timeLeft = Math.max(
      0,
      Math.floor(data.timer.next_penalty.time_remaining),
    );
    setNodeListText(timerElements, timeLeft + "s");

    // How much mood you lose next
    setNodeListText(penaltyElements, data.timer.next_penalty.amount);

    // How many timers/events are left
    setNodeListText(remainingElements, data.timer.timeline.events_remaining);
  }

  return data.state;
}

async function load_round() {
  const res = await fetch("/current_round");
  const data = await res.json();
  if (!data || !data.event) {
    return;
  }

  const question1 = document.querySelectorAll(".question-item-1");
  const question2 = document.querySelectorAll(".question-item-2");
  const question3 = document.querySelectorAll(".question-item-3");

  const questions = [question1, question2, question3];

  for (let i = 0; i < questions.length; i++) {
    if (i < data.event.length) {
      const q = data.event[i];
      setNodeListText(
        questions[i],
        `❓Vraag: ${q.question} \n 💰Uitgegeven budget: ${q.spent_budget ?? 0}`,
      );
    } else {
      setNodeListText(questions[i], "");
    }
  }
}
// ...existing code...

function setNodeListText(nodelist, text) {
  nodelist.forEach((curr_val) => {
    curr_val.innerText = text;
  });
}

async function startPolling() {
  try {
    const data = await load_game_state();
    const playerZones = document.querySelectorAll(".player-zone");

    if (data == "start") {
      // Show the green buttons
      playerZones.forEach((zone) => zone.classList.add("in-start-mode"));
      console.log("Waiting to start...");
    } else if (data == "running") {
      // Hide the green buttons and load the round
      playerZones.forEach((zone) => zone.classList.remove("in-start-mode"));
      load_round();
    }
  } catch (error) {
    console.error("Polling failed:", error);
  }

  setTimeout(startPolling, 200);
}

startPolling();
