from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path

from app.api.routes import router
from app.core.vectorstore import load_knowledge_base

load_dotenv()

app = FastAPI(
    title="AI Customer Support Agent API",
    description="RAG-powered support chatbot with memory and human escalation logic.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    load_knowledge_base()

# Mount API router
app.include_router(router, prefix="/api")

# Serve the HTML Chat Interface on root URL
@app.get("/", response_class=HTMLResponse)
def serve_chat_ui():
    html_path = Path("app/templates/index.html")
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Chatbot API Active. Access /docs for Swagger UI.</h1>")