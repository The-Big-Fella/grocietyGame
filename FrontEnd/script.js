async function loadState() {
    const res = await fetch("http://127.0.0.1:5000/api/state");
    const data = await res.json();

    // Vraag per zijde
    setWrappedText("q-north", data.question);
    setWrappedText("q-east", data.question);
    setWrappedText("q-south", data.question);
    setWrappedText("q-west", data.question);

    // Bevolking tevredenheid balk
const happiness = data.population_happiness;
const maxWidth = 40;
const barWidth = (happiness / 100) * maxWidth;

const bar = document.getElementById("happiness-bar");
bar.setAttribute("width", barWidth);
bar.setAttribute("fill", getHappinessColor(happiness));

updateTimerWarning(data.time_left);

}

// Kleur van de balk bepalen
function getHappinessColor(value) {
    if (value < 30) return "#e53935";
    if (value < 60) return "#fb8c00";
    return "#43a047";                   
}

// Tekst opdelen in regels
function setWrappedText(elementId, text, maxCharsPerLine = 22) {
    const textEl = document.getElementById(elementId);
    textEl.innerHTML = "";

    const words = text.split(" ");
    let line = "";
    let lineNumber = 0;

    words.forEach(word => {
        if ((line + word).length > maxCharsPerLine) {
            const tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
            tspan.setAttribute("x", textEl.getAttribute("x"));
            tspan.setAttribute("dy", lineNumber === 0 ? "0" : "3");
            tspan.textContent = line;
            textEl.appendChild(tspan);

            line = word + " ";
            lineNumber++;
        } else {
            line += word + " ";
        }
    });

    const tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
    tspan.setAttribute("x", textEl.getAttribute("x"));
    tspan.setAttribute("dy", lineNumber === 0 ? "0" : "3");
    tspan.textContent = line;
    textEl.appendChild(tspan);
}

// Timer pop-up
function updateTimerWarning(timeLeft) {
    const warning = document.getElementById("timer-warning");

    if (timeLeft <= 60 && timeLeft > 0) {
        warning.setAttribute("visibility", "visible");
    } else {
        warning.setAttribute("visibility", "hidden");
    }
}

setInterval(loadState, 500);
loadState();