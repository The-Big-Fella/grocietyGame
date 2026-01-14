const UPDATE_INTERVAL = 500;

let currentBudget = 0;
let roundStartTime = null;

// Update controllers visually
async function updateControllers() {
    try {
        const res = await fetch("/getcontroller");
        const data = await res.json();
        const container = document.getElementById("controller-list");
        container.innerHTML = "";

        Object.entries(data).forEach(([id, ctrl]) => {
            const div = document.createElement("div");
            div.className = "controller";
            div.innerHTML = `
                <div class="card-header">
                    <strong>Controller ${id}</strong>
                    <span class="badge ${ctrl.button_state ? 'active' : ''}">
                        ${ctrl.button_state ? "PRESSED" : "RELEASED"}
                    </span>
                </div>
                <div>Sliders: ${ctrl.sliders.join(" | ")}</div>
            `;
            container.appendChild(div);
        });
    } catch (err) {
        console.error(err);
    }
}

// Update round info: questions + sliders
async function updateRound() {
    try {
        const res = await fetch("/api/getcurrentround");
        const data = await res.json();
        const container = document.getElementById("round-info");

        if (!data || data.error) {
            container.innerHTML = `<div class="status-msg">Waiting for game start...</div>`;
            return;
        }

        currentBudget = data.round_budget;
        if (!roundStartTime) roundStartTime = Date.now();
        document.getElementById("round-budget").textContent = currentBudget;

        // Render questions
        let html = '';
        data.questions.forEach((q, index) => {
            html += `
                <div class="question-item">
                    <strong>Q${index + 1}:</strong> ${q.question}
                    <div class="slider-container">
                        <input type="range" min="0" max="${currentBudget}" value="0" step="1"
                               data-index="${index}" class="budget-slider">
                        <span>Allocated: <span class="slider-value">0</span></span>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;

        // Add slider behavior
        const sliders = container.querySelectorAll(".budget-slider");
        sliders.forEach(slider => {
            slider.addEventListener("input", () => {
                const value = parseInt(slider.value);

                // Calculate total allocation
                let totalAllocated = 0;
                sliders.forEach(s => totalAllocated += parseInt(s.value));

                // Cap slider if exceeds budget
                if (totalAllocated > currentBudget) {
                    slider.value = value - (totalAllocated - currentBudget);
                }

                // Update displayed allocated value
                slider.nextElementSibling.querySelector(".slider-value").textContent = slider.value;

                // Update budget display
                let allocated = 0;
                sliders.forEach(s => allocated += parseInt(s.value));
                document.getElementById("round-budget").textContent = currentBudget - allocated;
            });
        });

    } catch (err) {
        console.error(err);
    }
}

// Update round timer
function updateTimer() {
    if (roundStartTime) {
        const elapsed = Math.floor((Date.now() - roundStartTime) / 1000);
        document.getElementById("round-timer").textContent = elapsed;
    }
}

// Main loop
function updateLoop() {
    updateControllers();
    updateRound();
    updateTimer();
    updateMoodPenalties(); // <-- added here
    setTimeout(updateLoop, UPDATE_INTERVAL);
}

window.onload = updateLoop;

