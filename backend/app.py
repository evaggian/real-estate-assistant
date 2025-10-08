from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
import torch
import PyPDF2
import io
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
    CONTRACT_ANALYSIS_MAX_CHARS,
    CONTRACT_ANALYSIS_PROMPT_TEMPLATE,
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
    torch_dtype=torch.float16,  # Keep using torch_dtype for compatibility
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

@app.post("/upload-contract")
async def upload_contract(file: UploadFile = File(...)):
    """
    Upload and analyze a rental contract (PDF or TXT)
    """
    try:
        # Read file content
        content = await file.read()

        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif file.filename.endswith('.txt'):
            # Read text file
            text = content.decode('utf-8')
        else:
            return {"error": "Unsupported file type. Please upload PDF or TXT."}

        # Truncate if too long
        text_preview = text[:CONTRACT_ANALYSIS_MAX_CHARS] if len(text) > CONTRACT_ANALYSIS_MAX_CHARS else text

        # Create analysis prompt from template
        analysis_prompt = CONTRACT_ANALYSIS_PROMPT_TEMPLATE.format(contract_text=text_preview)

        # Add to chat history for context
        global chat_history
        chat_history.append({"role": "user", "content": f"[Contract uploaded: {file.filename}] Please analyze this contract."})

        # Format prompt
        prompt = f"System: {SYSTEM_PROMPT}\n\n"
        prompt += f"User: {analysis_prompt}\nAssistant:"

        # Generate analysis
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=250,  # Longer for detailed analysis
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            num_beams=1
        )

        # Decode response
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        analysis = full_response[len(tokenizer.decode(inputs.input_ids[0], skip_special_tokens=True)):].strip()

        # Add assistant response to history
        chat_history.append({"role": "assistant", "content": analysis})

        return {"analysis": analysis}

    except Exception as e:
        return {"error": f"Failed to process contract: {str(e)}"}


@app.get("/")
def root():
    return {
        "name": APP_NAME,
        "version": VERSION,
        "endpoints": {
            "chat": "/chat",
            "reset": "/reset",
            "health": "/health",
            "upload-contract": "/upload-contract"
        }
    }
