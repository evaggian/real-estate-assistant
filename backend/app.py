from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
import torch
from config import (
    VERSION,
    APP_NAME,
    APP_DESCRIPTION,
    MODEL_NAME,
    MAX_NEW_TOKENS,
    TEMPERATURE,
    API_HOST,
    API_PORT,
    CORS_ORIGINS,
    get_system_prompt
)

app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True
)
tokenizer.pad_token = tokenizer.eos_token


class Message(BaseModel):
    text: str

chat_history = []  # keep conversation in memory

SYSTEM_PROMPT = get_system_prompt()


@app.post("/chat")
def chat(message: Message):
    global chat_history

    # Add user message to history
    chat_history.append({"role": "user", "content": message.text})

    # Format prompt manually (chat template causing issues)
    prompt = f"System: {SYSTEM_PROMPT}\n\n"
    for msg in chat_history:
        role = "User" if msg['role'] == "user" else "Assistant"
        prompt += f"{role}: {msg['content']}\n"
    prompt += "Assistant:"

    # Generate response
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,  # Shorter responses for conciseness
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        num_beams=1  # Greedy decoding for speed
    )

    # Decode and extract reply
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    reply_text = full_response[len(tokenizer.decode(inputs.input_ids[0], skip_special_tokens=True)):].strip()

    # Add assistant response to history
    chat_history.append({"role": "assistant", "content": reply_text})

    return {"reply": reply_text}


@app.post("/reset")
def reset():
    global chat_history
    chat_history = []
    return {"status": "reset"}


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}

@app.get("/")
def root():
    return {
        "name": "Expat Rental Assistant API",
        "version": VERSION,
        "endpoints": {
            "chat": "/chat",
            "reset": "/reset",
            "health": "/health"
        }
    }
