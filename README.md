# AI Customer Support Agent (RAG + Multi-Turn Memory)

An enterprise-ready AI Customer Support Agent powered by **FastAPI**, **Groq (Llama 3.1)**, and **ChromaDB Vector Store**. The agent performs dynamic Retrieval-Augmented Generation (RAG), manages session conversation memory, evaluates vector distances for confidence scoring, triggers automated human escalation, and serves a live interactive Chatbot UI.

---

## 🛠️ Integrated Tools & APIs
1. **Groq LLM API (`llama-3.1-8b-instant`):** High-speed LLM engine for instruction-following and grounded customer support generation.
2. **ChromaDB Vector Store:** Embedded vector database used for semantic indexing and context retrieval.
3. **FastAPI Web Framework:** High-performance REST framework hosting the agent logic, health checks, and interactive HTML5 Chatbot interface.

---

## 📐 System Architecture & Workflow

```text
                               ┌───────────────────────────────────┐
                               │       Client / Chatbot UI         │
                               │  (HTML5 Frontend or REST API)     │
                               └─────────────────┬─────────────────┘
                                                 │
                                                 │ POST /api/chat
                                                 ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       FASTAPI AGENT SERVER                                       │
│                                                                                                  │
│   ┌───────────────────────────┐      ┌───────────────────────────┐     ┌──────────────────────┐  │
│   │ 1. Input Sanitization     ├─────►│ 2. Read Session Memory    ├────►│ 3. Vector RAG Search │  │
│   │    (Pydantic Schema)      │      │    (chat_history_db)      │     │    (ChromaDB Query)  │  │
│   └───────────────────────────┘      └───────────────────────────┘     └──────────┬───────────┘  │
│                                                                                   │              │
│   ┌───────────────────────────┐      ┌───────────────────────────┐                │              │
│   │ 6. Memory Store Update    │◄─────┤ 5. LLM Response Synthesis │◄───────────────┘              │
│   │    (Save User + Assistant)│      │    (Groq / Llama 3.1)     │  + Confidence & Escalation   │
│   └─────────────┬─────────────┘      └───────────────────────────┘    Distance Threshold Scoring │
└─────────────────┼────────────────────────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌───────────────────────────────────┐
│     JSON Client Response          │
│ {answer, escalate, session_id}    │

└───────────────────────────────────┘

---



## 🛡️ Error Handling & Fault Tolerance

The application enforces strict exception boundaries across all system components:

HTTP 400 (Bad Request): Validates empty queries, missing session IDs, or malformed JSON payloads using Pydantic schemas.

HTTP 500 (Internal Configuration Error): Gracefully intercepts missing server environment variables (GROQ_API_KEY) and returns structured JSON error responses.

HTTP 502 (Bad Gateway / Downstream Provider Failure): Traps external Groq API connection drops or network timeouts via explicit httpx exception wrapping.

Vector Store Fallback: If ChromaDB fails to match documents or encounters an exception, the system falls back to a neutral knowledge state and flags the session for human review (escalate: true).
 
 ## 🧪 Test Cases

Automated test cases are implemented using `pytest` and FastAPI's `TestClient` in `tests/test_agent.py`.

### 5 Core Test Scenarios

| Test Case | Scenario | Input Query | Expected Output & Assertion Logic |
| :--- | :--- | :--- | :--- |
| **TC-01** | **Direct FAQ Query** | `"How long does standard shipping take?"` | Retrieves exact FAQ answer (`3 to 5 business days`); returns `escalate: false`. |
| **TC-02** | **Semantic Vector Match** | `"When will my package arrive at my house?"` | Matches shipping policies using vector similarity without exact keyword overlap; returns `escalate: false`. |
| **TC-03** | **Multi-Turn Context Memory** | `"Can I speed that up?"` (Follow-up query) | Reads past turn from `chat_history_db`, understands "that" refers to shipping, and returns Express Shipping options. |
| **TC-04** | **Explicit Keyword Escalation** | `"I want to speak to a human manager immediately"` | Detects high-risk keyword `human`; sets `escalate: true`. |
| **TC-05** | **Out-of-Scope Fallback** | `"What is the orbital velocity of Jupiter?"` | Vector distance exceeds threshold cutoff (`> 1.8`); safely triggers `escalate: true`. |

### Running the Tests
To execute the automated test suite locally:
```bash
pytest tests/test_agent.py -v

---

## 🚀 Deployment Instructions

Option A: Local Development Setup
Clone the repository:

Bash
git clone https://github.com/LakshmiMeyyappan/ai-customer-support-agent.git
cd ai-customer-support-agent
Create virtual environment & install dependencies:

Bash
python -m venv custvenv
custvenv\Scripts\activate  # On Windows
# source custvenv/bin/activate # macOS/Linux

pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory:

Code snippet
GROQ_API_KEY=gsk_your_groq_api_key_here


## Launch Application:

Bash
uvicorn app.main:app --reload --port 8000
Live Chatbot UI: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Swagger API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Option B: Live Cloud Deployment (Render)
Live Web App & Chatbot UI: [https://ai-customer-support-agent.onrender.com/](https://ai-customer-support-agent.onrender.com/)

Swagger OpenAPI Docs: [https://ai-customer-support-agent.onrender.com/docs](https://ai-customer-support-agent.onrender.com/docs)