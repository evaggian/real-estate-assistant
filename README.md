# Real Estate Assistant

A conversational AI assistant for real estate inquiries, powered by Microsoft's DialoGPT model. This application features a FastAPI backend and a simple web-based chat interface.

## Features

- Interactive chat interface for real estate questions
- AI-powered responses using DialoGPT-medium model
- RESTful API backend with FastAPI
- Responsive web frontend
- Real-time conversation with context awareness

## Tech Stack

**Backend:**
- FastAPI
- Transformers (Hugging Face)
- PyTorch
- Microsoft DialoGPT-medium

**Frontend:**
- HTML/CSS/JavaScript
- Vanilla JS for chat interactions

## Project Structure

```
real-estate-assistant/
├── backend/
│   ├── app.py              # FastAPI application
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── index.html          # Chat interface
    ├── script.js           # Frontend logic
    └── style.css           # Styling
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Open `index.html` in a web browser, or use a local development server:
   ```bash
   # Using Python's built-in server
   python -m http.server 5500
   ```

3. Access the chat interface at `http://localhost:5500`

## Usage

1. Ensure the backend server is running
2. Open the frontend in your browser
3. Type your real estate questions in the chat input
4. Click "Send" or press Enter to receive AI-generated responses

## API Endpoints

### POST /chat

Send a message to the AI assistant.

**Request Body:**
```json
{
  "text": "Your question here"
}
```

**Response:**
```json
{
  "reply": "AI response"
}
```

## Notes

- The first request may take longer as the model needs to be loaded
- Chat history is maintained during the session
- CORS is configured to allow requests from localhost:5500

## License

MIT
