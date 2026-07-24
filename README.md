# 🤖 AI Customer Service Agent

An intelligent, multi-agent automated customer support system designed to handle inbound customer inquiries, perform automated issue resolution, route complex queries, and interface with backend knowledge bases. Built using cutting-edge Generative AI frameworks, LLMs, and API integrations, this agent delivers fast, accurate, and context-aware responses.

---

## 🛠️ Integrated Tools & Technologies

* **FastAPI:** High-performance REST framework hosting backend agent orchestration endpoints.
* **LangChain / Multi-Agent Framework:** Multi-agent routing logic enabling intelligent intent classification, context retention, and specialized task handling.
* **Groq / LLM Integration:** High-speed LLM inference for natural language understanding and contextual response generation.
* **ChromaDB Vector Store:** Embedded vector database enabling Retrieval-Augmented Generation (RAG) across customer knowledge bases, FAQs, and support documentation.
* **Streamlit / Swagger UI:** Interactive frontend interfaces for real-time customer chat interactions and developer testing.

---

## 📐 System Architecture & Workflow

```text
                               ┌──────────────────────────────────┐
                               │       Customer / User Client     │
                               │   (Web Portal / REST API / Chat) │
                               └────────────────┬─────────────────┘
                                                │
                                                │ Inbound Customer Query
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   AI CUSTOMER SERVICE AGENT SERVER                              │
│                                                                                                 │
│   ┌───────────────────────────┐      ┌───────────────────────────┐    ┌──────────────────────┐  │
│   │ 1. Intent Classification  ├─────►│ 2. Context Retrieval      ├───►│ 3. Specialized Agent  │  │
│   │    & Guardrail Checks     │      │    (ChromaDB RAG Engine)  │    │    Routing           │  │
│   └───────────────────────────┘      └───────────────────────────┘    └──────────┬───────────┘  │
│                                                                                  │              │
│   ┌───────────────────────────┐      ┌───────────────────────────┐               │              │
│   │ 6. Response Synthesis &   │◄─────┤ 5. Action Execution       │◄──────────────┘              │
│   │    Customer Resolution    │      │    (Tool & API Calls)     │   + 4. LLM Generation       │
│   └─────────────┬─────────────┘      └───────────────────────────┘     (Context-Aware Response) │
└─────────────────┼───────────────────────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌───────────────────────────────────┐
│     Structured Agent Response     │
│  {status, response, human_escal}  │
└───────────────────────────────────┘
```

---

## 🛡️ Error Handling & Fault Tolerance

The system incorporates robust safety guardrails and graceful error handling across all conversational paths:

* **HTTP 400 (Bad Request / Missing Payload):** Intercepts empty queries or malformed input objects immediately with clear diagnostic feedback.
* **Human Escalation Boundary:** Automatically detects frustrated sentiment or complex edge cases and flags the ticket for human agent takeover.
* **RAG Knowledge Base Fallback:** If vector retrieval confidence falls below a set threshold, the agent falls back to a polite clarification query rather than hallucinating answers.
* **API Rate Limit Guard:** Intercepts external LLM service timeouts or rate limits, returning structured fallback responses to maintain user engagement.

---

## 🧪 Test Cases & Automated Validation

The project includes an automated test suite executed via `pytest` to ensure prompt stability, retrieval accuracy, and endpoint resilience.

### 5 Core Test Scenarios

| Test Case | Scenario | Input Target | Expected Assertion & Validation |
| :--- | :--- | :--- | :--- |
| **TC-01** | **General Query Resolution** | Standard FAQ Question | Asserts HTTP status `200` and high-confidence, contextually relevant answer. |
| **TC-02** | **RAG Knowledge Retrieval** | Policy / Process Inquiry | Verifies accurate embedding search and citation of relevant internal documentation. |
| **TC-03** | **Human Escalation Trigger** | High Sentiment / Complex Issue | Asserts human escalation flag is set to `true` with routed summary. |
| **TC-04** | **Prompt Injection Prevention** | Adversarial / Jailbreak Input | Asserts guardrail detection blocks request without leaking system prompt or state. |
| **TC-05** | **Empty Payload Validation** | Blank Message Payload | Asserts HTTP status `400` or `422` validation handling without agent disruption. |

---

## 🚀 Deployment Instructions

### Option A: Local Development Setup
1. **Clone Repository & Navigate:**
   * `git clone https://github.com/YOUR_USERNAME/ai-customer-service-agent.git`
   * `cd ai-customer-service-agent`
2. **Create Virtual Environment & Install Dependencies:**
   * `python -m venv venv`
   * Activate environment: `venv\Scripts\activate` *(Windows)* or `source venv/bin/activate` *(macOS/Linux)*
   * `pip install -r requirements.txt`
3. **Set Environment Variables:**
   * Create a `.env` file in the root directory:
     ```env
     GROQ_API_KEY=your_groq_api_key_here
     ```
4. **Launch Application:**
   * `uvicorn app.main:app --reload --port 8000`
   * Interactive API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`

---

### Option B: Cloud Container Deployment (Render / Docker)
This application is fully containerized using Docker for production web hosting.

* **Live Web Endpoint:** `https://ai-customer-service-agent.onrender.com`
* **Live Interactive Playground (Swagger UI):** `https://ai-customer-service-agent.onrender.com/docs`
