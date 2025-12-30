"""
Vector Store for RAG (Retrieval-Augmented Generation)
Uses sentence-transformers for embeddings and ChromaDB for similarity search
"""

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import numpy as np
from typing import List, Tuple


class VectorStore:
    """Manages document embeddings and similarity search for RAG"""
    
    def __init__(self, collection_name: str = "sparrow_knowledge"):
        """
        Initialize the vector store with embedding model and ChromaDB
        
        Args:
            collection_name: Name of the ChromaDB collection
        """
        # Load the embedding model
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Initialize ChromaDB client (in-memory for simplicity)
        self.chroma_client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        
        # Create or get collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Captain Jack Sparrow knowledge base"}
        )
        
        print(f"Vector store initialized with collection: {collection_name}")
    
    def add_documents(self, documents: List[str]) -> None:
        """
        Add documents to the vector store
        
        Args:
            documents: List of text documents to add
        """
        if not documents:
            print("No documents to add")
            return
        
        print(f"Adding {len(documents)} documents to vector store...")
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents, show_progress_bar=True)
        
        # Add to ChromaDB
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=documents,
            ids=ids
        )
        
        print(f"Successfully added {len(documents)} documents")
    
    def query(self, query_text: str, n_results: int = 3) -> List[str]:
        """
        Query the vector store for similar documents
        
        Args:
            query_text: The query string
            n_results: Number of results to return
            
        Returns:
            List of most relevant document texts
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query_text])[0]
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        
        # Extract documents
        if results and results['documents']:
            return results['documents'][0]
        return []
    
    def load_from_file(self, filepath: str) -> None:
        """
        Load documents from a text file (one document per line)
        
        Args:
            filepath: Path to the text file
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                documents = [line.strip() for line in f if line.strip()]
            
            self.add_documents(documents)
            print(f"Loaded {len(documents)} documents from {filepath}")
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
        except Exception as e:
            print(f"Error loading file: {e}")


if __name__ == "__main__":
    # Test the vector store
    print("Testing VectorStore...")
    
    # Create vector store
    vs = VectorStore()
    
    # Add sample documents
    test_docs = [
        "Jack Sparrow is the captain of the Black Pearl.",
        "The Black Pearl is the fastest ship in the Caribbean.",
        "Jack's compass points to what you want most."
    ]
    vs.add_documents(test_docs)
    
    # Test query
    query = "Tell me about Jack's ship"
    results = vs.query(query, n_results=2)
    
    print(f"\nQuery: '{query}'")
    print("Results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")
