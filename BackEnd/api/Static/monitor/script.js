const UPDATE_INTERVAL = 500;

async function updateControllers() {
    try {
        const res = await fetch("/getcontroller");
        const data = await res.json();

        const container = document.getElementById("controller-list");
        if (!container) return;

        Object.entries(data).forEach(([id, ctrl]) => {
            let div = document.getElementById(`controller-${id}`);

            if (!div) {
                div = document.createElement("div");
                div.id = `controller-${id}`;
                div.className = "controller";
                container.appendChild(div);
            }

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
        });

        const existingIds = Object.keys(data);
        Array.from(container.children).forEach(child => {
            if (!existingIds.includes(child.id.replace("controller-", ""))) {
                container.removeChild(child);
            }
        });

    } catch (err) {
        console.error("Error fetching controllers:", err);
    }
}

async function updateLoop() {
    await updateControllers();
    setTimeout(updateLoop, UPDATE_INTERVAL);
    console.log("test")
}

window.onload = updateLoop;
