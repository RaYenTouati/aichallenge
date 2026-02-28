from fastapi import FastAPI, HTTPException
from app.schemas import QueryRequest, QueryResponse
from app.rag import UniHelpRAG
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="UniHelp API",
    description="Backend RAG pour assistant administratif universitaire",
    version="1.0.0"
)

# Initialisation du moteur RAG au démarrage
rag_engine = UniHelpRAG()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # origine React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"status": "ok", "message": "API UniHelp fonctionnelle."}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    try:
        if request.generate_email:
            result = rag_engine.generate_email(request.question)
        else:
            result = rag_engine.answer_question(request.question)
            
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            fallback_used=result["fallback_used"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
