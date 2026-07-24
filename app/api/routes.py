import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq
from app.core.vectorstore import collection

router = APIRouter()

# Simple in-memory session memory storage
chat_history_db = {}

# Pydantic Schemas
class ChatRequest(BaseModel):
    session_id: str
    query: str

class ChatResponse(BaseModel):
    session_id: str
    query: str
    answer: str
    escalate: bool
    confidence_note: str

@router.post("/chat", response_model=ChatResponse)
def support_agent_chat(request: ChatRequest):
    session_id = request.session_id
    user_query = request.query.strip()

    # 1. Initialize session memory if new user session
    if session_id not in chat_history_db:
        chat_history_db[session_id] = []

    # 2. Retrieve top matching chunks from ChromaDB (RAG)
    results = collection.query(
        query_texts=[user_query],
        n_results=2
    )

    retrieved_docs = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]
    context_text = "\n".join(retrieved_docs) if retrieved_docs else "No context available."

    # 3. Agent Escalation Logic
    escalate = False
    escalation_triggers = ["human", "agent", "supervisor", "refund", "stolen", "lawyer", "complaint"]
    
    # Trigger escalation if user requests it OR vector distance/confidence is poor
    if any(word in user_query.lower() for word in escalation_triggers):
        escalate = True
    elif distances and distances[0] > 1.5:  # Low retrieval match
        escalate = True

    # 4. Construct System Prompt with Memory and Context
    recent_memory = chat_history_db[session_id][-4:]  # Last 2 conversation turns
    history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_memory])

    system_prompt = f"""You are an empathetic, professional AI Customer Support Agent.
Answer the customer's question strictly using the Knowledge Base below.
If the answer is not available or if the user asks for human help, politely inform them that you are escalating the issue to a human support agent.

Knowledge Base Context:
{context_text}

Recent Conversation History:
{history_str}
"""

    # 5. Call Groq API (LLM)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable is missing.")

    client = Groq(
        api_key=api_key,
        http_client=httpx.Client(verify=False)  # Prevents local SSL connection issues
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    # 6. Save turn to Session Memory
    chat_history_db[session_id].append({"role": "user", "content": user_query})
    chat_history_db[session_id].append({"role": "assistant", "content": answer})

    return ChatResponse(
        session_id=session_id,
        query=user_query,
        answer=answer,
        escalate=escalate,
        confidence_note="High confidence FAQ match" if not escalate else "Escalation flagged for human review"
    )