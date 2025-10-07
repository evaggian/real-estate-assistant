document.getElementById("send-btn").addEventListener("click", async () => {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const message = input.value.trim();

  if (!message) return;

  chatBox.innerHTML += `<div class="user-msg">${message}</div>`;
  input.value = "";

  const response = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: message }),
  });

  const data = await response.json();
  chatBox.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
});
