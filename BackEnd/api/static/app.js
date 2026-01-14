const UPDATE_INTERVAL = 500; // Increased slightly for better performance

async function updateControllers() {
    try {
        const res = await fetch("/getcontroller");
        const data = await res.json();

        const container = document.getElementById("controller-list");
        // Only clear if data actually changed to prevent flickering
        container.innerHTML = "";

        // data is usually an object where keys are controller IDs
        Object.entries(data).forEach(([id, ctrl]) => {
            const div = document.createElement("div");
            div.className = "controller";
            div.innerHTML = `
                <div class="card-header">
                    <strong><i class="fas fa-gamepad"></i> Controller ${id}</strong>
                    <span class="badge ${ctrl.button_state ? 'active' : ''}">
                        ${ctrl.button_state ? "PRESSED" : "RELEASED"}
                    </span>
                </div>
                <div class="slider-info">
                    Sliders: ${ctrl.sliders.join(" | ")}
                </div>
            `;
            container.appendChild(div);
        });
    } catch (err) {
        console.error("Error fetching controllers:", err);
    }
}

async function updateRound() {
    try {
        // This endpoint should return the current state of your Round and QuestionList
        const res = await fetch("/api/getcurrentround");
        const data = await res.json();

        const container = document.getElementById("round-info");
        
        if (!data || data.error) {
            container.innerHTML = `<div class="status-msg">Waiting for game start...</div>`;
            return;
        }

        // data now represents your Round Node
        // Based on your Round class: { id: X, round_type: "...", event: [...] }
        let html = `
            <div class="round-card">
                <h3>${data.round_type} (ID: ${data.id})</h3>
                <div class="question-list">
        `;

        let html = `<strong>Round ${data.id}</strong><br>`;
        if (data.questions && data.questions.length) {
            html += "<ul>";
            data.questions.forEach(q => {
                html += `<li>${q.question} | Mood: ${q.mood} | Time: ${q.time}</li>`;
            });
        } else {
            html += `<p>No questions loaded for this round.</p>`;
        }

        html += `</div></div>`;
        container.innerHTML = html;

    } catch (err) {
        console.error("Error fetching round:", err);
    }
}

function updateLoop() {
    updateControllers();
    updateRound();
    setTimeout(updateLoop, UPDATE_INTERVAL);
}

window.onload = updateLoop;
