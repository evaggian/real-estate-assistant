// Automatically detect API endpoint (local vs Docker)
const API_URL = "http://localhost:8000";

console.log("Using API URL:", API_URL);

const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const clearBtn = document.getElementById("clear-btn");
const suggestions = document.getElementById("suggestions");

// Restore chat history on page load
window.addEventListener("load", () => {
  const saved = localStorage.getItem("chatHistory");
  if (saved) {
    chatBox.innerHTML = saved;
    // Hide suggestions if there's existing chat
    suggestions.style.display = "none";
  } else {
    // Show welcome message and suggestions on first load
    showWelcomeMessage();
    suggestions.style.display = "flex";
  }
});

// Welcome message
function showWelcomeMessage() {
  const time = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  chatBox.innerHTML = `
    <div class="self-start bg-blue-50 rounded-lg px-3 py-2 max-w-[80%] border-l-4 border-blue-400">
      <p class="text-xs text-blue-600 font-semibold mb-1">Bay</p>
      <p class="text-sm">👋 Welcome, I am Bay. I help expats navigate the Dutch rental market. Try the suggestions below or ask me anything!</p>
      <span class="text-xs text-gray-500 ml-2">${time}</span>
    </div>`;
}

// Save chat history before page unload
window.addEventListener("beforeunload", () => {
  localStorage.setItem("chatHistory", chatBox.innerHTML);
});

// --- Markdown rendering function ---
function renderMarkdown(text) {
  return text
    // Bold: **text** or __text__
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/__(.+?)__/g, '<strong>$1</strong>')
    // Italic: *text* or _text_
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/_(.+?)_/g, '<em>$1</em>')
    // Bullet points: - item or * item
    .replace(/^[\-\*]\s+(.+)$/gm, '<li>$1</li>')
    // Wrap lists in <ul>
    .replace(/(<li>.*<\/li>\s*)+/gs, match => `<ul class="list-disc ml-4 my-2">${match}</ul>`)
    // Line breaks
    .replace(/\n/g, '<br>');
}

// --- Typing effect function with markdown support ---
async function typeText(element, text, speed = 15) {
  // Split text into chunks (words and punctuation)
  const chunks = text.match(/[\w']+|[.,!?;:\-\n]|\s+/g) || [text];
  let fullText = '';

  for (let chunk of chunks) {
    fullText += chunk;
    element.innerHTML = renderMarkdown(fullText);
    chatBox.scrollTop = chatBox.scrollHeight;

    // Slight delay for natural typing feel
    if (chunk.trim()) {
      await new Promise(resolve => setTimeout(resolve, speed));
    }
  }
}

// --- Send message ---
async function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  const time = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  // Add user message
  chatBox.innerHTML += `
    <div class="self-end bg-green-100 text-right rounded-lg px-3 py-2 max-w-[80%] ml-auto animate-fadeIn border-l-4 border-green-600">
      ${message}<span class="text-xs text-gray-500 ml-2">${time}</span>
    </div>`;
  input.value = "";

  // Show typing indicator
  chatBox.innerHTML += `
    <div class="self-start bg-blue-50 rounded-lg px-3 py-2 max-w-[80%] animate-pulse border-l-4 border-blue-400">
      <em>Assistant is typing...</em>
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

    // Replace typing indicator with empty message container
    typingElem.outerHTML = `
      <div class="bot-message self-start bg-blue-50 rounded-lg px-3 py-2 max-w-[80%] animate-fadeIn border-l-4 border-blue-400 relative group">
        <span class="message-text"></span><span class="text-xs text-gray-500 ml-2">${time}</span>
        <button class="copy-btn absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition-opacity bg-blue-200 hover:bg-blue-300 rounded px-2 py-1 text-xs" title="Copy response">📋</button>
      </div>`;

    // Get the new message element
    const botMessage = chatBox.querySelector(".bot-message:last-child .message-text");

    // Simulate typing effect by displaying text gradually
    await typeText(botMessage, data.reply);

    // Add copy functionality
    const copyBtn = chatBox.querySelector(".bot-message:last-child .copy-btn");
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(botMessage.textContent);
      copyBtn.textContent = "✓";
      setTimeout(() => copyBtn.textContent = "📋", 2000);
    });

  } catch (error) {
    typingElem.outerHTML = `
      <div class="self-start bg-red-100 text-red-700 rounded-lg px-3 py-2 max-w-[80%] animate-fadeIn border-l-4 border-red-500">
        Error: ${error.message}
      </div>`;
  }

  chatBox.scrollTop = chatBox.scrollHeight;
  localStorage.setItem("chatHistory", chatBox.innerHTML);
}

// --- Event listeners ---
sendBtn.addEventListener("click", sendMessage);

// Enter to send, Shift+Enter for new line
input.addEventListener("keypress", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Suggestion buttons
document.querySelectorAll(".suggestion-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const text = btn.textContent.trim();
    input.value = text;
    sendMessage();
    // Hide suggestions after first use
    suggestions.style.display = "none";
  });
});

// --- Clear chat + reset backend context ---
clearBtn.addEventListener("click", async () => {
  chatBox.innerHTML = "";
  localStorage.removeItem("chatHistory");

  try {
    await fetch(`${API_URL}/reset`, { method: "POST" });
  } catch (err) {
    console.warn("Failed to reset backend:", err.message);
  }

  // Show welcome message and suggestions again
  showWelcomeMessage();
  suggestions.style.display = "flex";
});