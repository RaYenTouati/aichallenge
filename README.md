# UniHelp - Assistant IA pour Services Administratifs Universitaires

## 1. Architecture du Système

**UniHelp** repose sur une architecture RAG (Retrieval-Augmented Generation) classique mais robuste pour répondre aux questions des étudiants en se basant *uniquement* sur les documents officiels de l'université.

1. **Ingestion des documents** : Les PDF (règlements, FAQ, procédures) sont extraits à l'aide de `PyPDFLoader`.
2. **Chunking** : Le texte est découpé en segments (chunks) avec un algorithme optimisé pour préserver le contexte (ex: 1000 caractères, 200 de chevauchement).
3. **Embeddings** : Chaque segment est transformé en vecteur via `sentence-transformers` (gratuit et local) ou OpenAI.
4. **Base Vectorielle** : Les vecteurs sont stockés dans **FAISS** (base locale, extrêmement rapide, sans coût d'hébergement, parfaite pour un hackathon).
5. **Recherche (Retrieval)** : À chaque question, la query est vectorisée et comparée à la base FAISS pour extraire les Top-K passages les plus pertinents et leur score de similitude (confiance).
6. **Génération (Generation)** : Un LLM (OpenAI GPT-4o-mini ou GPT-3.5) reçoit les passages pertinents en plus de la question + un **Prompt strict anti-hallucination**. Il formule la réponse.
7. **Emails automatiques** : Un endpoint ou bouton spécifique permet d'utiliser le même contexte pour générer un brouillon d'email administratif pré-formaté.

## 2. Explication du pipeline RAG

Le principe du RAG est de palier le manque de connaissances spécifiques d'un LLM et de limiter ses hallucinations.
Au lieu de poser directement la question au LLM :
- Nous cherchons d'abord dans les documents de l'Université les paragraphes qui parlent par exemple des "absences justifiées".
- Nous donnons ces paragraphes au LLM en lui disant : *"Tu es un assistant. Réponds à la question uniquement grâce au texte suivant."*
- Le LLM génère une phrase fluide en reprenant nos documents.

## 3. Structure du Projet

```text
UniHelp/
├── data/
│   ├── raw/                 # Placez vos PDF officiels ici
│   └── vectordb/            # Index FAISS généré automatiquement
├── app/
│   ├── api.py               # Serveur FastAPI (Backend)
│   ├── indexer.py           # Script pour indexer les documents dans FAISS
│   ├── rag.py               # Logique coeur du RAG (Search + Gen)
│   ├── prompts.py           # Templates de prompts (Anti-hallucination, Emails)
│   └── schemas.py           # Modèles Pydantic de l\'API
├── frontend/
│   └── streamlit_app.py     # Interface utilisateur intuitive avec Streamlit
├── requirements.txt         # Dépendances Python
└── PITCH.md                 # Scénarios de démo et pitch
```

## Comment exécuter le projet ?

1. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Configurer les variables d'environnement**
Créez un fichier `.env` à la racine (ou définissez la variable) :
```env
OPENAI_API_KEY=sk-...
```

3. **Placer des documents**
Mettez quelques PDF dans `data/raw/` (ex: règlement des études). S'il n'y a pas de documents, créez un PDF de test simple.

4. **Indexer les documents (générer la base vectorielle)**
```bash
python -m app.indexer
```

5. **Lancer le Backend (FastAPI)**
```bash
python -m uvicorn app.api:app --reload --port 8000
```

6. **Lancer le Frontend (Streamlit)**
Dans un nouveau terminal :
```bash
streamlit run frontend/streamlit_app.py
```
