function sendMessage() {
    const input = document.getElementById("symptomInput");
    const symptoms = input.value.trim();
    const patientName = document.getElementById("patientName").value.trim();

    if (!symptoms) return;

    // Show user message with patient name if provided
    const label = patientName ? `${patientName}: ${symptoms}` : symptoms;
    addMessage(label, "user");
    input.value = "";

    const typingId = showTyping();

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: symptoms, patient: patientName })
    })
    .then(response => response.json())
    .then(data => {
        removeTyping(typingId);
        displayBotResponse(data);
    })
    .catch(error => {
        removeTyping(typingId);
        addMessage("Connection error. Please try again.", "bot");
    });
}

function addMessage(text, sender) {
    const chatbox = document.getElementById("chatbox");
    const div = document.createElement("div");
    div.className = sender === "user" ? "user-message" : "bot-message";
    div.innerText = text;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function displayBotResponse(data) {
    const chatbox = document.getElementById("chatbox");
    const div = document.createElement("div");
    div.className = "bot-message";

    // Extract potency from dosage for badge
    function getPotency(dosage) {
        const match = dosage.match(/\d+[CcMmXx]+/);
        return match ? match[0].toUpperCase() : "OTC";
    }

    // Condition header
    div.innerHTML = `
        <div class="condition-header">
            <div>
                <div class="condition-label">Likely Condition</div>
                <div class="condition-name">🩺 ${data.condition}</div>
            </div>
        </div>

        <div class="section-label">Homeopathic Remedies</div>
    `;

    // Medicine cards
    data.medicines.forEach(med => {
        div.innerHTML += `
            <div class="medicine-card">
                <div>
                    <div class="med-name">🌿 ${med.name}</div>
                    <div class="med-dosage">${med.dosage}</div>
                </div>
                <span class="potency-badge">${getPotency(med.dosage)}</span>
            </div>
        `;
    });

    // Lifestyle advice
    if (data.lifestyle) {
        div.innerHTML += `
            <div class="section-label">Lifestyle</div>
            <div class="advice-box">🧘 ${data.lifestyle}</div>
        `;
    }

    // General advice
    div.innerHTML += `
        <div class="section-label">Advice</div>
        <div class="advice-box">💡 ${data.advice}</div>
    `;

    // Doctor warning
    if (data.see_doctor) {
        div.innerHTML += `
            <div class="doctor-warning">
                🏥 <span>${data.doctor_reason}</span>
            </div>
        `;
    }

    // Disclaimer
    div.innerHTML += `
        <div class="disclaimer">⚠️ Educational use only. Not real medical advice. Always consult a licensed homeopathic doctor.</div>
    `;

    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function showTyping() {
    const chatbox = document.getElementById("chatbox");
    const div = document.createElement("div");
    div.className = "typing";
    div.id = "typing-" + Date.now();
    div.innerHTML = `<span></span><span></span><span></span>`;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
    return div.id;
}

function removeTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

document.getElementById("symptomInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});
