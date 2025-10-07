// Automatically detect API endpoint (local vs Docker)
const API_URL = window.location.hostname.includes("localhost")
  ? "http://127.0.0.1:8000"
  : "http://backend:8000";

console.log("Using API URL:", API_URL);

const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const clearBtn = document.getElementById("clear-btn");

// Restore chat history on page load
window.addEventListener("load", () => {
  const saved = localStorage.getItem("chatHistory");
  if (saved) chatBox.innerHTML = saved;
});

// Save chat history before page unload
window.addEventListener("beforeunload", () => {
  localStorage.setItem("chatHistory", chatBox.innerHTML);
});

// --- Send message ---
async function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  const time = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  // Add user message
  chatBox.innerHTML += `
    <div class="self-end bg-blue-100 text-right rounded-lg px-3 py-2 max-w-[80%] ml-auto animate-fadeIn">
      ${message}<span class="text-xs text-gray-500 ml-2">${time}</span>
    </div>`;
  input.value = "";

  // Show typing indicator
  chatBox.innerHTML += `
    <div class="self-start bg-gray-100 rounded-lg px-3 py-2 max-w-[80%] animate-pulse">
      <em>Bot is typing...</em>
    </div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
  const typingElem = chatBox.lastChild;

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: message }),
    });

    const data = await response.json();

    // Replace typing indicator with actual reply
    typingElem.outerHTML = `
      <div class="self-start bg-gray-100 rounded-lg px-3 py-2 max-w-[80%] animate-fadeIn">
        ${data.reply}<span class="text-xs text-gray-500 ml-2">${time}</span>
      </div>`;
  } catch (error) {
    typingElem.outerHTML = `
      <div class="self-start bg-red-100 text-red-700 rounded-lg px-3 py-2 max-w-[80%] animate-fadeIn">
        Error: ${error.message}
      </div>`;
  }

  chatBox.scrollTop = chatBox.scrollHeight;
  localStorage.setItem("chatHistory", chatBox.innerHTML);
}

// --- Event listeners ---
sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", e => { if (e.key === "Enter") sendMessage(); });

// --- Clear chat + reset backend context ---
clearBtn.addEventListener("click", async () => {
  chatBox.innerHTML = "";
  localStorage.removeItem("chatHistory");

  try {
    await fetch(`${API_URL}/reset`, { method: "POST" });
  } catch (err) {
    console.warn("Failed to reset backend:", err.message);
  }

  chatBox.innerHTML += `
    <div class="text-center text-gray-400 text-sm mt-2">
      Chat cleared.
    </div>`;
});