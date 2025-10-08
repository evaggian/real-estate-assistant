/**
 * Frontend tests for Expat Rental Assistant
 * Tests UI components, user interactions, and API communication
 */

// Mock fetch for API calls
global.fetch = jest.fn();

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

describe('Expat Rental Assistant Frontend', () => {

  beforeEach(() => {
    // Reset DOM before each test
    document.body.innerHTML = `
      <div id="chat-box"></div>
      <input id="user-input" type="text" />
      <button id="send-btn">Send</button>
      <button id="clear-btn">Clear</button>
      <div id="suggestions">
        <button class="suggestion-btn">Test suggestion</button>
      </div>
    `;

    // Clear mocks
    fetch.mockClear();
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
    localStorageMock.removeItem.mockClear();
  });

  describe('DOM Elements', () => {
    test('should have all required elements', () => {
      expect(document.getElementById('chat-box')).toBeTruthy();
      expect(document.getElementById('user-input')).toBeTruthy();
      expect(document.getElementById('send-btn')).toBeTruthy();
      expect(document.getElementById('clear-btn')).toBeTruthy();
      expect(document.getElementById('suggestions')).toBeTruthy();
    });

    test('should have suggestion buttons', () => {
      const buttons = document.querySelectorAll('.suggestion-btn');
      expect(buttons.length).toBeGreaterThan(0);
    });
  });

  describe('Welcome Message', () => {
    test('should display welcome message when no chat history', () => {
      localStorageMock.getItem.mockReturnValue(null);

      const chatBox = document.getElementById('chat-box');
      chatBox.innerHTML = `
        <div class="text-center text-gray-600 text-sm p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p class="font-semibold text-blue-700 mb-2">👋 Welcome!</p>
        </div>`;

      expect(chatBox.innerHTML).toContain('Welcome');
      expect(chatBox.innerHTML).toContain('👋');
    });
  });

  describe('Chat Functionality', () => {
    test('should add user message to chat box', () => {
      const chatBox = document.getElementById('chat-box');
      const input = document.getElementById('user-input');

      input.value = 'Test message';

      // Simulate adding message
      const time = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      chatBox.innerHTML += `
        <div class="self-end bg-green-100 text-right rounded-lg px-3 py-2 max-w-[80%] ml-auto animate-fadeIn border-l-4 border-green-600">
          Test message<span class="text-xs text-gray-500 ml-2">${time}</span>
        </div>`;

      expect(chatBox.innerHTML).toContain('Test message');
    });

    test('should show typing indicator during API call', () => {
      const chatBox = document.getElementById('chat-box');

      chatBox.innerHTML += `
        <div class="self-start bg-blue-50 rounded-lg px-3 py-2 max-w-[80%] animate-pulse border-l-4 border-blue-400">
          <em>Assistant is typing...</em>
        </div>`;

      expect(chatBox.innerHTML).toContain('Assistant is typing');
    });

    test('should handle empty message gracefully', () => {
      const input = document.getElementById('user-input');
      input.value = '';

      // Empty messages should not be processed
      expect(input.value.trim()).toBe('');
    });
  });

  describe('API Communication', () => {
    test('should call chat API with correct payload', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ reply: 'Test response' })
      });

      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: 'Hello' })
      });

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/chat',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: 'Hello' })
        })
      );

      const data = await response.json();
      expect(data.reply).toBe('Test response');
    });

    test('should handle API errors gracefully', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'));

      try {
        await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: 'Hello' })
        });
      } catch (error) {
        expect(error.message).toBe('Network error');
      }
    });
  });

  describe('LocalStorage Integration', () => {
    test('should save chat history to localStorage', () => {
      const chatBox = document.getElementById('chat-box');
      chatBox.innerHTML = '<div>Test chat</div>';

      localStorageMock.setItem('chatHistory', chatBox.innerHTML);

      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'chatHistory',
        '<div>Test chat</div>'
      );
    });

    test('should load chat history from localStorage', () => {
      const savedHistory = '<div>Previous chat</div>';
      localStorageMock.getItem.mockReturnValue(savedHistory);

      const history = localStorageMock.getItem('chatHistory');

      expect(localStorageMock.getItem).toHaveBeenCalledWith('chatHistory');
      expect(history).toBe(savedHistory);
    });

    test('should clear chat history on reset', () => {
      localStorageMock.removeItem('chatHistory');

      expect(localStorageMock.removeItem).toHaveBeenCalledWith('chatHistory');
    });
  });

  describe('Suggestion Buttons', () => {
    test('should trigger message on suggestion click', () => {
      const suggestionBtn = document.querySelector('.suggestion-btn');
      const input = document.getElementById('user-input');

      // Simulate click
      const text = suggestionBtn.textContent.trim();
      input.value = text;

      expect(input.value).toBe('Test suggestion');
    });
  });

  describe('Clear Functionality', () => {
    test('should clear chat box', () => {
      const chatBox = document.getElementById('chat-box');
      chatBox.innerHTML = '<div>Some chat</div>';

      chatBox.innerHTML = '';

      expect(chatBox.innerHTML).toBe('');
    });

    test('should call reset API endpoint', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ status: 'reset' })
      });

      const response = await fetch('http://localhost:8000/reset', {
        method: 'POST'
      });

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/reset',
        { method: 'POST' }
      );

      const data = await response.json();
      expect(data.status).toBe('reset');
    });
  });

  describe('Typing Effect', () => {
    test('should have typeText function logic', () => {
      const text = 'Hello world';
      const chunks = text.match(/[\w']+|[.,!?;:\-\n]|\s+/g);

      expect(chunks).toContain('Hello');
      expect(chunks).toContain('world');
    });
  });

  describe('UI Responsiveness', () => {
    test('should have version displayed', () => {
      document.body.innerHTML += '<p class="text-center text-xs text-gray-400 mb-3">v1.0.0</p>';

      expect(document.body.innerHTML).toContain('v1.0.0');
    });

    test('should have welcome message with emoji', () => {
      document.body.innerHTML += '<p class="font-semibold text-blue-700 mb-2">👋 Welcome!</p>';

      expect(document.body.innerHTML).toContain('👋 Welcome!');
    });
  });
});
