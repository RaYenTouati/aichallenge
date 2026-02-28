import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.prompts import UNIHELP_PROMPT, EMAIL_PROMPT
from app.schemas import SourceInfo

load_dotenv()

VECTOR_DB_DIR = "data/vectordb"

class UniHelpRAG:
    def __init__(self):
        # 1. Charger les embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 2. Charger la base vectorielle FAISS
        try:
            self.vector_store = FAISS.load_local(
                VECTOR_DB_DIR, 
                self.embeddings,
                allow_dangerous_deserialization=True # Requis par la lib FAISS
            )
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
            self.db_loaded = True
        except Exception as e:
            print(f"Attention: Impossible de charger la base FAISS. Avez-vous exécuté app/indexer.py ? Erreur: {e}")
            self.db_loaded = False
            
        # 3. Initialiser le LLM (OpenAI par défaut)
        # L'utilisateur a fourni une clé OpenRouter, nous devons donc changer l'URL de base
        self.llm = ChatOpenAI(
            model="openai/gpt-4o-mini", # OpenRouter requiert souvent le préfixe du provider
            temperature=0,
            base_url="https://openrouter.ai/api/v1"
        )

    def format_docs(self, docs):
        """Formate les chunks récupérés pour le prompt LLM."""
        return "\n\n".join(
            f"[Source: {doc.metadata.get('source', 'Inconnu')} - Page {doc.metadata.get('page', '?')}]\n{doc.page_content}"
            for doc in docs
        )

    def retrieve_context(self, question: str):
        """Recherche (Retrieval) FAISS avec calcul de Confiance."""
        if not self.db_loaded:
            return [], "La base de données documentaire n'est pas initialisée."
            
        # find matching documents with scores (lower score = higher similarity)
        docs_and_scores = self.vector_store.similarity_search_with_score(question, k=4)
        
        sources = []
        for doc, score in docs_and_scores:
            # Score de similitude arbitraire converti en pourcentage pour le frontend
            confidence = max(0.0, 100.0 - (score * 50)) 
            
            sources.append(SourceInfo(
                document_name=os.path.basename(doc.metadata.get("source", "Document Inconnu")),
                content_snippet=doc.page_content[:150] + "...",
                confidence_score=round(confidence, 1)
            ))
            
        # extraire les documents purs pour la génération
        docs = [doc for doc, _ in docs_and_scores]
        formatted_context = self.format_docs(docs)
        
        return sources, formatted_context

    def answer_question(self, question: str) -> dict:
        """Pipeline RAG (Génération de la Réponse)."""
        sources, context = self.retrieve_context(question)
        
        if not self.db_loaded:
             return {
                "answer": "Serveur non initialisé (Base de données vectorielle introuvable). Exécutez l'indexation.",
                "sources": [],
                "fallback_used": True
            }



        # Pipeline Langchain: Prompt -> LLM -> Output text
        chain = UNIHELP_PROMPT | self.llm | StrOutputParser()
        answer = chain.invoke({"context": context, "question": question})
        
        # Vérification anti-hallucination (Le LLM a-t-il appelé le fallback ?)
        fallback_used = "Désolé, je ne trouve pas cette information" in answer

        return {
            "answer": answer,
            "sources": sources,
            "fallback_used": fallback_used
        }

    def generate_email(self, question: str) -> dict:
        """Génération d'email administratif selon le contexte."""
        sources, context = self.retrieve_context(question)
        
        if not self.db_loaded or len(sources) == 0:
            return {
                "answer": "Impossible de générer l'email : aucune procédure pertinente trouvée dans les documents officiels.",
                "sources": [],
                "fallback_used": True
            }

        chain = EMAIL_PROMPT | self.llm | StrOutputParser()
        email_draft = chain.invoke({"context": context, "question": question})

        return {
            "answer": email_draft,
            "sources": sources,
            "fallback_used": False
        }
