import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

DATA_DIR = "data/raw"
VECTOR_DB_DIR = "data/vectordb"

def build_index():
    print("🚀 Début de l'indexation des documents...")
    
    # 1. Vérification des dossiers
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
    
    if not pdf_files:
        print(f"⚠️ Aucun fichier PDF trouvé dans {DATA_DIR}.")
        print("Veuillez ajouter des documents officiels pour construire la base de connaissances.")
        return

    documents = []
    
    # 2. Chargement des documents
    for file in pdf_files:
        file_path = os.path.join(DATA_DIR, file)
        print(f"📄 Chargement de {file}...")
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
        
    print(f"✅ {len(documents)} pages chargées au total.")
    
    # 3. Chunking (texte split)
    print("✂️ Découpage des documents en segments...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Documents découpés en {len(chunks)} segments (chunks).")
    
    # 4. Modèle d'Embeddings
    # Utilisation d'un modèle gratuit, local et rapide (idéal hackathon)
    print("🧠 Initialisation du modèle d'embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 5. Création et Sauvegarde de la base FAISS
    print("💾 Création de l'index FAISS (Vector DB)...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(VECTOR_DB_DIR)
    
    print("🎉 Indexation terminée avec succès ! La base vectorielle est prête.")

if __name__ == "__main__":
    build_index()
