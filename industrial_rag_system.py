import os
import json
from typing import List, Dict, Tuple, Optional
from openai import OpenAI
import pdfplumber
import chromadb
from pathlib import Path


class IndustrialRAGSystem:
    """
    Production-ready RAG system for industrial regulatory documents
    Supports multiple PDFs with source tracking and metadata filtering
    """
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        """
        Initialize the Industrial RAG system
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model for completions
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.embedding_model = "text-embedding-3-small"
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = None
        self.collection_name = "aer_directives"
        
        # Document registry
        self.documents = {}
        
        print(f"Industrial RAG System initialized")
        print(f"Model: {self.model}")
        print(f"Vector Database: ChromaDB")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        print(f"Extracting text from {pdf_path}...")
        text = ""
        
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            for i, page in enumerate(pdf.pages):
                if (i + 1) % 50 == 0:
                    print(f"  Processing page {i + 1}/{total_pages}...")
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        
        print(f"  Extracted {len(text):,} characters from {total_pages} pages")
        return text
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            # Break at sentence boundaries
            if end < len(text):
                last_period = max(
                    chunk_text.rfind('.'),
                    chunk_text.rfind('?'),
                    chunk_text.rfind('!')
                )
                
                if last_period > chunk_size * 0.5:
                    chunk_text = chunk_text[:last_period + 1]
                    end = start + last_period + 1
            
            if chunk_text.strip():
                chunks.append(chunk_text.strip())
            
            start = end - overlap
        
        return chunks
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings using OpenAI API"""
        print(f"Creating embeddings for {len(texts)} chunks...")
        
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(texts) - 1) // batch_size + 1
            print(f"  Batch {batch_num}/{total_batches}")
            
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=batch
            )
            
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
        
        print(f"  Created {len(all_embeddings)} embeddings")
        return all_embeddings
    
    def add_document(self, pdf_path: str, document_name: str, document_type: str):
        """
        Add a document to the RAG system
        
        Args:
            pdf_path: Path to PDF file
            document_name: Human-readable name (e.g., "Directive 001")
            document_type: Category (e.g., "Compliance", "Safety", "Measurement")
        """
        print(f"\n{'='*60}")
        print(f"Processing: {document_name}")
        print(f"Type: {document_type}")
        print(f"{'='*60}")
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        
        # Chunk text
        print(f"Chunking text (size=500, overlap=100)...")
        chunks = self.chunk_text(text, chunk_size=500, overlap=100)
        print(f"  Created {len(chunks)} chunks")
        
        # Store document info
        doc_id = Path(pdf_path).stem
        self.documents[doc_id] = {
            'name': document_name,
            'type': document_type,
            'path': pdf_path,
            'chunks': len(chunks)
        }
        
        return chunks, doc_id
    
    def build_index(self, documents: List[Dict]):
        """
        Build vector index from multiple documents
        
        Args:
            documents: List of dicts with keys: 'path', 'name', 'type'
                Example: [
                    {'path': 'directive_001.pdf', 'name': 'Directive 001', 'type': 'Compliance'},
                    {'path': 'directive_017.pdf', 'name': 'Directive 017', 'type': 'Measurement'}
                ]
        """
        print("\n" + "="*60)
        print("BUILDING MULTI-DOCUMENT VECTOR INDEX")
        print("="*60)
        
        # Collect all chunks and metadata
        all_chunks = []
        all_metadatas = []
        chunk_global_id = 0
        
        for doc in documents:
            chunks, doc_id = self.add_document(
                doc['path'],
                doc['name'],
                doc['type']
            )
            
            # Add metadata for each chunk
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadatas.append({
                    'document_id': doc_id,
                    'document_name': doc['name'],
                    'document_type': doc['type'],
                    'chunk_index': i,
                    'source_file': doc['path']
                })
                chunk_global_id += 1
        
        print(f"\n{'='*60}")
        print(f"Total chunks across all documents: {len(all_chunks)}")
        print(f"{'='*60}")
        
        # Create embeddings
        embeddings = self.create_embeddings(all_chunks)
        
        # Create or recreate ChromaDB collection
        try:
            self.chroma_client.delete_collection(name=self.collection_name)
            print(f"\nDeleted existing collection: {self.collection_name}")
        except:
            pass
        
        self.collection = self.chroma_client.create_collection(
            name=self.collection_name,
            metadata={"description": "AER Directives multi-document index"}
        )
        print(f"Created new collection: {self.collection_name}")
        
        # Add to ChromaDB
        print(f"\nAdding documents to ChromaDB...")
        ids = [f"chunk_{i}" for i in range(len(all_chunks))]
        
        self.collection.add(
            embeddings=embeddings,
            documents=all_chunks,
            metadatas=all_metadatas,
            ids=ids
        )
        
        print(f"\n{'='*60}")
        print("INDEX BUILD COMPLETE")
        print(f"{'='*60}")
        print(f"Total documents: {len(documents)}")
        print(f"Total chunks: {len(all_chunks)}")
        print(f"Embedding dimensions: {len(embeddings[0])}")
        print(f"Storage: ./chroma_db/")
        
        # Print document breakdown
        print(f"\nDocument Breakdown:")
        for doc_id, info in self.documents.items():
            print(f"  - {info['name']}: {info['chunks']} chunks ({info['type']})")
    
    def load_index(self):
        """Load existing ChromaDB collection"""
        print(f"Loading ChromaDB collection: {self.collection_name}...")
        
        try:
            self.collection = self.chroma_client.get_collection(name=self.collection_name)
            count = self.collection.count()
            print(f"✓ Collection loaded: {count} chunks")
            
            # Reconstruct document registry from metadata
            sample = self.collection.get(limit=1000, include=['metadatas'])
            if sample and sample['metadatas']:
                for meta in sample['metadatas']:
                    doc_id = meta.get('document_id')
                    if doc_id and doc_id not in self.documents:
                        self.documents[doc_id] = {
                            'name': meta.get('document_name', 'Unknown'),
                            'type': meta.get('document_type', 'Unknown'),
                            'path': meta.get('source_file', ''),
                            'chunks': 0
                        }
                
                # Count chunks per document
                for meta in sample['metadatas']:
                    doc_id = meta.get('document_id')
                    if doc_id in self.documents:
                        self.documents[doc_id]['chunks'] += 1
            
            print(f"✓ Loaded {len(self.documents)} documents")
            
        except Exception as e:
            raise ValueError(f"Failed to load collection: {e}")
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        document_filter: Optional[str] = None
    ) -> List[Tuple[str, float, Dict]]:
        """
        Search for relevant chunks
        
        Args:
            query: Search query
            top_k: Number of results
            document_filter: Optional document name to filter by
            
        Returns:
            List of (chunk_text, score, metadata) tuples
        """
        if self.collection is None:
            raise ValueError("Collection not loaded")
        
        # Create query embedding
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=[query]
        )
        query_embedding = response.data[0].embedding
        
        # Build filter
        where_filter = None
        if document_filter and document_filter != "All Documents":
            where_filter = {"document_name": document_filter}
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter
        )
        
        # Format results
        chunks = results['documents'][0]
        distances = results['distances'][0]
        metadatas = results['metadatas'][0]
        
        # Convert to similarity scores
        max_dist = max(distances) if distances else 1.0
        similarities = [1 - (d / max_dist) if max_dist > 0 else 1.0 for d in distances]
        
        return list(zip(chunks, similarities, metadatas))
    
    def generate_response(
        self,
        query: str,
        top_k: int = 5,
        document_filter: Optional[str] = None
    ) -> Dict:
        """Generate response using RAG"""
        
        # Retrieve relevant chunks
        results = self.search(query, top_k, document_filter)
        
        # Build context
        context_parts = []
        for i, (chunk, score, metadata) in enumerate(results, 1):
            doc_name = metadata.get('document_name', 'Unknown')
            context_parts.append(
                f"[Source {i} - {doc_name}] (Relevance: {score:.2f}):\n{chunk}"
            )
        
        context = "\n\n".join(context_parts)
        
        # System prompt
        system_message = """You are an expert assistant for Alberta Energy Regulator (AER) directives and industrial compliance.

Your role:
- Answer questions based ONLY on the provided AER directive excerpts
- Provide accurate, compliance-focused information
- Include specific directive references when relevant
- If information is not in the context, clearly state this
- Be professional and precise

Guidelines:
- Cite specific directives when answering
- Include relevant section numbers if mentioned in context
- Keep answers clear and actionable
- Do not make up requirements not in the context"""
        
        # User prompt
        user_message = f"""Context from AER Directives:

{context}

Question: {query}

Provide a clear, professional answer based on the context above. Include relevant directive citations."""
        
        # Generate response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,  # Lower temperature for factual compliance info
            max_tokens=600
        )
        
        answer = response.choices[0].message.content
        
        return {
            'answer': answer,
            'sources': [
                {
                    'chunk': chunk,
                    'relevance': score,
                    'document': metadata.get('document_name'),
                    'type': metadata.get('document_type')
                }
                for chunk, score, metadata in results
            ],
            'context': context
        }
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        if self.collection is None:
            return {"error": "Collection not loaded"}
        
        total_chunks = self.collection.count()
        
        return {
            'total_chunks': total_chunks,
            'total_documents': len(self.documents),
            'documents': self.documents,
            'collection_name': self.collection_name,
            'embedding_model': self.embedding_model,
            'chat_model': self.model
        }


def main():
    """Build the multi-document index"""
    import sys
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set")
        print("Run: export OPENAI_API_KEY='your-key'")
        sys.exit(1)
    
    # Initialize system
    rag = IndustrialRAGSystem(api_key=api_key)
    
    # Define documents to process
    documents = [
        {
            'path': 'directive_001.pdf',
            'name': 'Directive 001',
            'type': 'Site-Specific Liability'
        },
        {
            'path': 'directive_017.pdf',
            'name': 'Directive 017',
            'type': 'Measurement Requirements'
        }
    ]
    
    # Check files exist
    for doc in documents:
        if not os.path.exists(doc['path']):
            print(f"ERROR: {doc['path']} not found")
            print(f"\nPlease download the PDF first:")
            print(f"  curl -o {doc['path']} https://static.aer.ca/prd/documents/directives/{doc['path'].replace('_', '').replace('.pdf', '.pdf')}")
            sys.exit(1)
    
    # Build index
    rag.build_index(documents)
    
    # Display stats
    stats = rag.get_stats()
    print(f"\n{'='*60}")
    print("SYSTEM READY")
    print(f"{'='*60}")
    print(f"Run: python3 app.py")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
