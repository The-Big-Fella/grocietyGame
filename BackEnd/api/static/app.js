// Update interval (ms)
const UPDATE_INTERVAL = 200;

// Fetch and display controller state
async function updateControllers() {
    try {
        const res = await fetch("/getcontroller");
        const data = await res.json();

        const container = document.getElementById("controller-list");
        container.innerHTML = "";

        for (const [id, ctrl] of Object.entries(data)) {
            const div = document.createElement("div");
            div.className = "controller";
            div.innerHTML = `
                <strong>Controller ${id}</strong><br>
                Sliders: ${ctrl.sliders.join(", ")}<br>
                Button: ${ctrl.button_state ? "Pressed" : "Released"}
            `;
            container.appendChild(div);
        }
    } catch (err) {
        console.error("Error fetching controllers:", err);
    }
}

// Fetch and display current round state
async function updateRound() {
    try {
        const res = await fetch("/getcurrentround");
        const data = await res.json();

        const container = document.getElementById("round-info");
        container.innerHTML = "";

        if (!data) {
            container.textContent = "No active round";
            return;
        }

        const div = document.createElement("div");
        div.className = "round";

        let html = `<strong>Round ${data.id}</strong><br>`;
        if (data.questions && data.questions.length) {
            html += "<ul>";
            data.questions.forEach(q => {
                html += `<li>${q.question} | Mood: ${q.mood} | Budget: ${q.budget} | Time: ${q.time}</li>`;
            });
            html += "</ul>";
        }
        div.innerHTML = html;
        container.appendChild(div);

    } catch (err) {
        console.error("Error fetching round:", err);
    }
}

// Main update loop
function updateLoop() {
    updateControllers();
    updateRound();
    setTimeout(updateLoop, UPDATE_INTERVAL);
}

// Start updating after page loads
window.onload = updateLoop;
