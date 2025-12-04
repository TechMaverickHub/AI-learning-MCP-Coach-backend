# rag_store.py
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# NEW Chroma persistent client
chroma_client = chromadb.PersistentClient(path="./chroma_store")

# Create or load collection
collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

def add_document(doc_id: str, text: str):
    """Add a document & embedding to Chroma."""
    embedding = embedder.encode(text).tolist()
    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding]
    )

def search_documents(query: str, top_k: int = 5):
    """Semantic search from Chroma."""
    query_emb = embedder.encode(query).tolist()

    result = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )

    return result["documents"][0] if result["documents"] else []
