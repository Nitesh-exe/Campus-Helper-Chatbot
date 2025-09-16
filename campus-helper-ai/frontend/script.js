const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatbox = document.getElementById("chatbox");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    appendMessage("user", message);
    input.value = "";
    scrollToBottom();

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            appendMessage("bot", "Sorry, something went wrong. Please try again.");
            scrollToBottom();
            return;
        }

        const data = await response.json();
        appendMessage("bot", data.reply);
        scrollToBottom();
    } catch (error) {
        appendMessage("bot", "Error connecting to the server.");
        scrollToBottom();
    }
});

function appendMessage(sender, text) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.textContent = text;
    chatbox.appendChild(msgDiv);
}

function scrollToBottom() {
    chatbox.scrollTop = chatbox.scrollHeight;
}
