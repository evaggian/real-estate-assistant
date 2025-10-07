from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_name = "facebook/blenderbot-400M-distill"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


class Message(BaseModel):
    text: str

chat_history = ""  # keep conversation in memory


@app.post("/chat")
def chat(message: Message):
    global chat_history
    chat_history += f"User: {message.text}\nBot: "
    inputs = tokenizer.encode(chat_history, return_tensors="pt")
    outputs = model.generate(inputs, max_length=600, pad_token_id=tokenizer.eos_token_id)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    reply_text = reply.split("Bot:")[-1].strip()
    chat_history += f"{reply_text}\n"
    return {"reply": reply_text}


@app.post("/reset")
def reset():
    global chat_history
    chat_history = ""
    return {"status": "reset"}


@app.get("/health")
def health():
    return {"status": "ok"}
