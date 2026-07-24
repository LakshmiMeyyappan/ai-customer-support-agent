import json
from pathlib import Path
import chromadb

# Initialize local in-memory ChromaDB client
client = chromadb.Client()
collection = client.get_or_create_collection(name="customer_support_kb")

def load_knowledge_base():
    """Populates ChromaDB with JSON and Markdown FAQ data on app start."""
    if collection.count() > 0:
        return  # Data already loaded

    documents = []
    metadatas = []
    ids = []
    idx = 0

    # 1. Load JSON FAQs
    json_path = Path("data/faq_data.json")
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            faqs = json.load(f)
            for item in faqs:
                documents.append(item["answer"])
                metadatas.append({"question": item["question"], "category": item.get("category", "faq")})
                ids.append(f"doc_{idx}")
                idx += 1

    # 2. Load Markdown Policy docs
    md_path = Path("data/shopify_shipping.md")
    if md_path.exists():
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
            chunks = [c.strip() for c in md_content.split("\n\n") if c.strip()]
            for chunk in chunks:
                documents.append(chunk)
                metadatas.append({"question": "General Policy", "category": "markdown_doc"})
                ids.append(f"doc_{idx}")
                idx += 1

    # Insert into ChromaDB
    if documents:
        collection.add(documents=documents, metadatas=metadatas, ids=ids)