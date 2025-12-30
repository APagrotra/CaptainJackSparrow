# Captain Jack Sparrow AI Chatbot

> "Not all treasure is silver and gold, mate." - Captain Jack Sparrow

## Character Description
This is an AI chatbot with the persona of **Captain Jack Sparrow** from Pirates of the Caribbean. The bot speaks with Jack's signature wit, unpredictable mannerisms, and pirate vocabulary. It has knowledge about Jack's adventures, the Black Pearl, and pirate lore.

## Implementation Overview

### 🔍 RAG (Retrieval-Augmented Generation)
- **Knowledge Base**: 20+ facts about Jack Sparrow stored in `data/sparrow_facts.txt`
- **Vector Store**: Uses `sentence-transformers` for embeddings and `chromadb` for similarity search
- **Retrieval**: Fetches relevant facts based on user queries to enhance responses

### 🧠 Memory System
- **Conversation History**: Maintains sliding window of last N conversation turns
- **Context Awareness**: Remembers user information shared during conversation
- **Formatted Storage**: Stores messages in structured format for context injection

### 🧮 Advanced Technique: Calculator Tool
- **Mathematical Operations**: Can evaluate arithmetic expressions
- **Use Case**: Perfect for counting gold doubloons, pieces of eight, or calculating navigation coordinates
- **Safe Evaluation**: Uses safe expression parsing to avoid code injection

## Project Structure
```
AIOT HW Week15/
├── data/
│   └── sparrow_facts.txt       # Knowledge base facts
├── src/
│   ├── vector_store.py         # RAG implementation
│   ├── memory.py               # Conversation memory
│   ├── tools.py                # Calculator tool
│   └── chatbot.py              # Main bot logic
├── main.py                     # CLI interface
├── requirements.txt            # Dependencies
├── .env.example                # API key template
└── README.md                   # This file
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your Google Gemini API key
# GEMINI_API_KEY=your_gemini_key_here
```

### 3. Run the Chatbot
```bash
python main.py
```

## Usage Examples

**Persona Interaction:**
```
You: Who are you?
Jack: Captain Jack Sparrow, savvy? The one and only!
```

**Knowledge Retrieval (RAG):**
```
You: Tell me about the Black Pearl
Jack: *retrieves fact from knowledge base about the Black Pearl*
```

**Calculator Tool:**
```
You: Calculate 100 pieces of eight times 3
Jack: *uses calculator* That be 300 pieces of eight, mate!
```

**Memory:**
```
You: My name is Elizabeth
Jack: Pleasure to meet ye, Elizabeth!
... conversation continues ...
You: What's my name?
Jack: Elizabeth, if me memory serves me right!
```

## Reflection & Assessment

### What Worked Well
- **Persona Consistency**: The system prompt effectively maintains Captain Jack's voice. The distinct vocabulary ("savvy", "mate", "arr") and rambling style make interactions engaging.
- **RAG Integration**: The vector store successfully retrieves specific facts (like the Black Pearl's speed or Jack's debts) and the bot weaves them naturally into the pirate persona.
- **Calculator Tool**: The tool successfully handles math queries in-character ("pieces of eight"), adding dynamic utility to the bot.
- **Offline Fallback**: Implementing the offline mode (mock mode) ensured the project was demonstrable even without a working API key initially, showing robust error handling.

### What Didn't Work / Challenges
- **API Key Issues**: Initially faced challenges with invalid OpenAI keys. This was resolved by migrating to the Google Gemini API (Free Tier), which proved to be a reliable alternative.
- **Response Length**: The initial prompts led to overly long, rambling responses. We had to refine the system instruction definition to strictly limit response length for better user experience.
- **Unicode Support**: Windows terminal had issues displaying pirate emojis (🏴‍☠️), which was fixed by forcing UTF-8 encoding in the Python script.

### Final Thoughts
This project successfully demonstrates the core components of a modern LLM application: **retrieval** (RAG), **memory** (conversation history), and **action** (tools). By wrapping these technical features in a strong persona (Captain Jack Sparrow), the interaction becomes entertaining rather than just functional. The transition to Gemini API showed the flexibility of the architecture to switch LLM providers with minimal code changes.

## Grading Rubric Checklist

### Character Choice
- [x] Character: Captain Jack Sparrow from Pirates of the Caribbean
- [x] Clear persona with distinctive speaking style
- [x] Documented in README

### RAG Implementation
- [x] Knowledge base with 20+ facts (`data/sparrow_facts.txt`)
- [x] Vector embeddings using `sentence-transformers`
- [x] Vector store for similarity search (`chromadb`)
- [x] Query retrieval integrated into responses

### Memory System
- [x] Conversation history tracking
- [x] Context-aware responses
- [x] Sliding window memory management

### Code Quality
- [x] Clean, modular code structure
- [x] Proper class organization
- [x] Error handling

### Documentation
- [x] Comprehensive README
- [x] Setup instructions
- [x] Usage examples
- [x] Project structure documented
- [x] Reflection and Analysis included

## Technical Details

**LLM Integration**: Google Gemini API (`gemini-flash-latest`)

**Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`

**Vector Store**: ChromaDB for efficient similarity search

**Memory Window**: Last 10 conversation turns (configurable)

---

*"In the End... This is the day you will always remember as the day you almost caught Captain Jack Sparrow!😁"*

