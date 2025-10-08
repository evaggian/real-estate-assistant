# Expat Rental Assistant 🇳🇱🏠

A specialized conversational AI assistant helping international professionals and families navigate the Dutch rental market. Powered by Alibaba's Qwen2.5-1.5B-Instruct with a custom-built web chat interface.

**Target Users:** Expats relocating to the Netherlands (Amsterdam, Utrecht, Rotterdam, The Hague, etc.)

## Features

- **Specialized Expat Focus** - Tailored advice for international renters
- **Comprehensive Coverage** - Neighborhoods, contracts, visas, utilities, deposits
- **AI-powered responses** using Qwen2.5-1.5B-Instruct model with custom system prompt
- **RESTful API backend** with FastAPI
- **Custom-built responsive frontend** (no pre-existing chat frameworks)
- **Contextual continuity** - model remembers conversation history
- **Chat history persistence** - saved in browser localStorage
- **Timestamped messages** for better UX
- **One-command deployment** using Docker Compose

### What the Assistant Helps With:
- 🏘️ Expat-friendly neighborhoods and areas
- 📝 Rental contracts and legal requirements (huurcontract, huurcommissie)
- 🛂 Visa and residency considerations (BSN, residence permit)
- 🌐 Cultural differences in Dutch rental markets
- 🛋️ Furnished vs unfurnished rentals
- 💰 Utilities (G/W/E), deposits, and service costs
- 👥 Expat community resources and international schools
- 🚇 Transportation (OV-chipkaart, cycling culture)

### Special Features:

#### 💰 **Price Fairness Checker**
Ask about rental prices and get instant feedback based on 2024 market averages:
- *"Is €1,400 for a 1-bedroom in Utrecht fair?"*
- Bot provides context: typical ranges for Amsterdam, Utrecht, Rotterdam, The Hague
- Mentions utility costs and factors affecting pricing
- Helps avoid overpaying or suspiciously low prices

#### 📋 **Document Checklist Generator**
Get a complete checklist of required documents for renting:
- *"What documents do I need to rent in the Netherlands?"*
- Bot provides detailed list: BSN, proof of income, bank account, etc.
- Explains what each document is and how to obtain it
- Tailored for expats (includes residence permit info for non-EU)

#### ⚠️ **Scam Detection Warning**
Describes a suspicious situation and get fraud prevention advice:
- *"Landlord wants deposit before I see the property"*
- Bot flags common scam patterns and red flags
- Provides safety tips and verification steps
- References trusted platforms (Funda, Pararius, Kamernet)

## Tech Stack

**Backend:**
- **FastAPI** - Modern Python web framework for REST API
- **Transformers** (Hugging Face) - For loading and running the LLM
- **PyTorch** - Deep learning framework
- **Qwen2.5-1.5B-Instruct** (Alibaba Cloud) - Small, fast instruction-following model
- **Uvicorn** - ASGI server

**Frontend:**
- **HTML5/CSS3** - Structure and styling
- **Vanilla JavaScript** - No frameworks, pure JS for chat interactions
- **Tailwind CSS** - Utility-first CSS framework for responsive design
- **LocalStorage API** - For chat history persistence

**DevOps:**
- **Docker** & **Docker Compose** - Containerization and orchestration
- **Python HTTP Server** - Serving static frontend files

## Project Structure

```
real-estate-assistant/
├── backend/
│   ├── app.py              # FastAPI application with model integration
│   ├── test_app.py         # Comprehensive test suite
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Multi-stage Docker build with tests
├── frontend/
│   ├── index.html          # Custom chat interface
│   ├── script.js           # Chat logic & API integration
│   └── Dockerfile          # Frontend container configuration
├── docker-compose.yml      # Multi-container orchestration
├── docker-compose.test.yml # Test-only configuration
├── .dockerignore           # Docker build exclusions
└── README.md               # This file
```

## Version

**Current Version:** v1.0.0

## Quick Start (Docker - Recommended)

### Prerequisites
- **Docker** and **Docker Compose** installed
- At least **8GB RAM** available
- **6GB free disk space** for model download

### Build and Run

**Single command to start everything:**

```bash
docker-compose up --build
```

This will:
1. Build both backend and frontend containers
2. Download the Qwen2.5-1.5B-Instruct model (~3GB)
3. Start both services
4. Backend: `http://localhost:8000`
5. Frontend: `http://localhost:5500`

**Access the application:**
Open your browser and go to `http://localhost:5500`

**Stop the application:**
```bash
docker-compose down
```

---

## Alternative: Local Development Setup (Without Docker)

### Prerequisites
- Python 3.12+
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

2. Start a local development server:
   ```bash
   python -m http.server 5500
   ```

3. Access the chat interface at `http://localhost:5500`

---

## Usage

1. Open `http://localhost:5500` in your browser
2. Type your real estate questions in the chat input
3. Click "Send" or press **Enter** to receive AI-generated responses
4. Click "Clear" to reset the conversation history
5. Chat history is automatically saved in your browser

## API Endpoints

### POST /chat
Send a message to the AI assistant.

**Request Body:**
```json
{
  "text": "What are the key factors to consider when buying a house?"
}
```

**Response:**
```json
{
  "reply": "When buying a house, consider factors like location, budget, size, condition..."
}
```

### POST /reset
Reset the conversation history.

**Response:**
```json
{
  "status": "reset"
}
```

### GET /health
Check if the backend is running.

**Response:**
```json
{
  "status": "ok"
}
```

---

## Creative Choices & UX Design

This project includes several creative decisions designed to enhance user experience, build trust, and make the interface feel approachable and professional.

### 🎨 Visual Design & Branding

#### **Color Scheme: Green & Blue Real Estate Theme**
- **Green accents** (`#059669`) convey growth, trust, and nature - aligning with real estate industry standards
- **Blue tones** suggest reliability and professionalism
- Gradient background (`green-50` to `blue-50`) creates a calm, welcoming atmosphere
- Color-coded suggestion buttons (green for pricing, blue for documents, red for scam warnings) provide visual categorization

#### **Bubble-Style Interface**
- Rounded pill-shaped buttons (`rounded-full`) for suggestions and action buttons create a modern, friendly appearance
- Chat bubbles with rounded corners feel conversational and approachable
- Buttons auto-size to text content, avoiding unnecessary visual clutter
- Centered, wrapped layout allows suggestions to flow naturally

#### **Subtle Branding**
- Version and company name (`brainbay • v1.0.0`) placed at bottom in tiny, light gray text (9px) - visible for debugging but not intrusive
- Clean header design focuses on the assistant's name rather than corporate branding

### 🤖 Personality & Friendliness

#### **Named Assistant: "Bay"**
- Personal name creates emotional connection and makes the bot feel less robotic
- "Bay" derives from "brainbay" company name - reinforcing brand identity subtly
- Introduces herself in first person ("Welcome, I am Bay") to establish personality
- Name appears above each bot message for consistent identity

#### **Conversational Welcome Message**
- Welcome message styled as a bot response bubble (not a generic banner) to immediately establish conversational tone
- Direct introduction ("I am Bay") humanizes the interaction
- Mentions key value proposition upfront: "help expats navigate the Dutch rental market"
- Encourages action with "Try the suggestions below or ask me anything!"

### 💬 UX Enhancements

#### **Pre-selected Quick Suggestions**
- Three example questions demonstrate the bot's capabilities immediately
- Cover the three special features (price check, document list, scam detection)
- Help users who don't know what to ask or are new to Dutch rentals
- Disappear after first interaction to avoid clutter
- Reappear when chat is cleared for easy restart

#### **"Assistant is typing..." Indicator**
- Shows while waiting for AI response to prevent confusion
- Prevents users from thinking the app is frozen or broken
- Creates natural conversation rhythm and sets expectations
- Pulsing animation adds subtle motion feedback

#### **Typing Effect Animation**
- Bot responses appear word-by-word (15ms delay) instead of instantly
- Mimics human typing speed for more natural conversation feel
- Gives users time to read and process information gradually
- Makes wait time feel productive rather than stuck

#### **Markdown Rendering**
- Supports **bold text**, *italics*, and bullet lists in bot responses
- Makes structured information (like document checklists) easier to scan
- Improves readability without manual HTML formatting
- Lists automatically styled with disc bullets and proper spacing

#### **Copy Button on Messages**
- Each bot response has a clipboard button (appears on hover)
- Allows users to save important info (addresses, document lists, price ranges)
- Shows checkmark (✓) confirmation when copied
- Subtle placement (top-right corner) doesn't distract from message content

#### **Enter to Send + Keyboard Support**
- Press **Enter** to send message (Shift+Enter for line breaks)
- Reduces friction - no need to move mouse to "Send" button
- Familiar pattern from messaging apps
- Improves accessibility and typing workflow

#### **Consistent Typography**
- All interactive elements use `text-sm` (14px) for readability
- Input placeholder provides helpful example without being verbose
- Name labels use smaller `text-xs` blue text to differentiate from message content
- Timestamps in light gray don't compete with message text

### Frontend Innovations:
1. **Chat History Persistence** - Uses browser localStorage to save chat history across sessions
2. **Timestamped Messages** - Each message shows the time it was sent
3. **Auto-scroll** - Automatically scrolls to newest messages
4. **Fade-in Animations** - Smooth message appearance using CSS animations
5. **Responsive Design** - Works on different screen sizes using Tailwind CSS
6. **Clear Button** - Resets both frontend and backend conversation context
7. **Error Handling** - Displays user-friendly error messages

### Backend Features:
1. **Contextual Continuity** - Maintains full conversation history for context-aware responses
2. **Optimized Model Loading** - Uses FP16 precision for 2x memory reduction
3. **Proper Chat Formatting** - Uses Qwen's chat template for better instruction following
4. **CORS Support** - Allows frontend-backend communication
5. **Health Check Endpoint** - For monitoring service status
6. **Embedded Market Data** - 2024 rental price averages for major Dutch cities
7. **Smart Scam Detection** - Pattern-based fraud warning system
8. **Document Knowledge Base** - Complete Dutch rental document requirements

### Model Selection:
- **Qwen2.5-1.5B-Instruct** was chosen for:
  - Small size (~3GB) - fast download and startup
  - Excellent instruction-following capabilities
  - No authentication required (Apache 2.0 license)
  - Optimized for local inference
  - Better quality than generic chatbots for specialized Q&A

### Domain Specialization:
- **Custom System Prompt** guides the model to focus specifically on expat rental scenarios
- Helps redirect off-topic queries (e.g., buying property) back to rentals
- Provides consistent, focused advice tailored to international relocators
- Understands common expat challenges (visa requirements, cultural differences, etc.)

---

## Performance Notes

- **First request**: May take 30-60 seconds as the model loads into memory
- **Subsequent requests**: ~5-15 seconds on CPU (faster on GPU)
- **Model download**: ~3GB, happens automatically on first run
- **Memory usage**: ~4-6GB RAM for model inference
- **GPU support**: Automatically uses CUDA if available for 10x faster inference

---

## Testing

Comprehensive test suites for both backend and frontend ensure code quality and reliability.

### Run Tests with Docker (Recommended)

Tests are automatically run during Docker build to ensure code quality:

```bash
# Run all tests (backend + frontend)
docker-compose -f docker-compose.test.yml build

# Run only backend tests
docker-compose -f docker-compose.test.yml build backend-test

# Run only frontend tests
docker-compose -f docker-compose.test.yml build frontend-test
```

The multi-stage Dockerfiles run tests before building production images, ensuring only tested code is deployed.

### Run Tests Locally

**Backend Tests:**
```bash
cd backend
pip install -r requirements.txt
pytest test_app.py -v
```

**Frontend Tests:**
```bash
cd frontend
npm install
npm test
```

### Test Coverage

**Backend Tests (Python/Pytest):**
- **API Endpoint Tests** - Root, health, chat, reset endpoints
- **Feature Tests** - Price checker, document checklist, scam detection
- **Context Persistence** - Conversation history management
- **Error Handling** - Empty messages, invalid inputs

**Frontend Tests (JavaScript/Jest):**
- **DOM Elements** - Verifies all UI components exist
- **Welcome Message** - Tests initial user experience
- **Chat Functionality** - User messages, typing indicators
- **API Communication** - Fetch calls, error handling
- **LocalStorage** - Chat history persistence
- **UI Interactions** - Suggestion buttons, clear functionality
- **Typing Effect** - Text animation logic

### Example Test Output

```
test_app.py::test_root_endpoint PASSED
test_app.py::test_health_endpoint PASSED
test_app.py::test_chat_endpoint_structure PASSED
test_app.py::test_price_fairness_feature PASSED
test_app.py::test_document_checklist_feature PASSED
test_app.py::test_scam_detection_feature PASSED
```

---

## Troubleshooting

**Model download is slow:**
- The model is downloaded from Hugging Face on first run
- Check your internet connection
- Download happens inside the Docker container

**Backend not responding:**
- Check if backend container is running: `docker ps`
- View backend logs: `docker logs chat_backend`
- Ensure port 8000 is not in use

**Frontend cannot connect to backend:**
- Ensure both containers are running
- Check browser console for errors
- Verify backend is accessible at `http://localhost:8000/health`

---

## License

MIT
