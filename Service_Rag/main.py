from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

app = FastAPI(title="RAG Retrieval API")

CHROMA_PATH = "./chroma_db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Initialize embeddings and ChromaDB globally so they are ready on startup
try:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
except Exception as e:
    print(f"Warning: Could not load ChromaDB. Did you run ingest.py? Error: {e}")
    db = None

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class DocumentResponse(BaseModel):
    content: str
    metadata: dict

class QueryResponse(BaseModel):
    results: list[DocumentResponse]

@app.post("/retrieve", response_model=QueryResponse)
async def retrieve_context(request: QueryRequest):
    if db is None:
        raise HTTPException(status_code=500, detail="ChromaDB is not initialized.")
    
    # Perform similarity search
    docs = db.similarity_search(request.query, k=request.top_k)
    
    results = []
    for doc in docs:
        results.append(DocumentResponse(
            content=doc.page_content,
            metadata=doc.metadata
        ))
        
    return QueryResponse(results=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
