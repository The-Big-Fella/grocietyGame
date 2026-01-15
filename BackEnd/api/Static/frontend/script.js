async function load_game_state() {
  const res = await fetch("/game_state");
  const data = await res.json();

  let moodElement = document.querySelectorAll("#mood");
  let budgetElement = document.querySelectorAll("#budget");
  setNodeListText(moodElement, data.mood);
  setNodeListText(budgetElement, data.budget);
}

async function load_round() {
  const res = await fetch("/current_round");
  const data = await res.json();
  if (!data) {
    return;
  }

  const question1 = document.querySelectorAll(".question-item-1");
  const question2 = document.querySelectorAll(".question-item-2");
  const question3 = document.querySelectorAll(".question-item-3");

  const questions = [question1, question2, question3];

  for (let i = 0; i < questions.length; i++) {
    for (let j = 0; j < data.event.length; j++) {
      let event = data.event[j];
      setNodeListText(
        questions[i],
        `${event.question} | ${event.mood} | ${event.budget}`,
      );
    }
  }
}

function setNodeListText(nodelist, text) {
  nodelist.forEach((curr_val) => {
    curr_val.innerText = text;
  });
}

load_game_state();
load_round();
