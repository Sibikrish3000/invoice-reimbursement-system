import chromadb
from chromadb.config import Settings
from app.core.config import settings
from app.api.models.invoice import InvoiceAnalysis
import json
from typing import List, Dict, Any
import os

class VectorStore:
    def __init__(self):
        # Ensure the vector store directory exists
        os.makedirs(settings.VECTOR_STORE_PATH, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=settings.VECTOR_STORE_PATH,
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name="invoice_analyses",
            metadata={"hnsw:space": "cosine"}
        )

    def store_analysis(self, analysis: InvoiceAnalysis) -> None:
        """Store an invoice analysis in the vector store."""
        # Convert analysis to dictionary
        analysis_dict = analysis.model_dump()

        # Convert all datetime fields to ISO strings and lists/dicts to JSON strings
        for key, value in analysis_dict.items():
            if isinstance(value, (list, dict)):
                analysis_dict[key] = json.dumps(value)
            elif hasattr(value, 'isoformat'):
                analysis_dict[key] = value.isoformat()

        # Create document text for embedding
        doc_text = f"""
        Invoice Analysis for {analysis.employee_name}
        Status: {analysis.status}
        Total Amount: {analysis.total_amount}
        Reimbursable Amount: {analysis.reimbursable_amount}
        Reason: {analysis.reason}
        Policy Violations: {', '.join(analysis.policy_violations) if analysis.policy_violations else 'None'}
        """
        
        # Store in vector database
        self.collection.add(
            ids=[analysis.invoice_id],
            documents=[doc_text],
            metadatas=[analysis_dict]
        )

    def search_analyses(
        self,
        query: str,
        n_results: int = 5,
        where: Dict[str, Any] = None
    ) -> List[InvoiceAnalysis]:
        """Search for invoice analyses using semantic search and metadata filtering."""
        # Perform the search
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )
        
        # Convert results back to InvoiceAnalysis objects
        analyses = []
        for metadata in results['metadatas'][0]:
            # Parse JSON string fields back to Python objects
            for key, value in metadata.items():
                if isinstance(value, str):
                    try:
                        parsed = json.loads(value)
                        # Only replace if parsed is list or dict
                        if isinstance(parsed, (list, dict)):
                            metadata[key] = parsed
                    except (json.JSONDecodeError, TypeError):
                        pass
            analysis = InvoiceAnalysis(**metadata)
            analyses.append(analysis)
        
        return analyses

    def get_analysis_by_id(self, invoice_id: str) -> InvoiceAnalysis:
        """Retrieve a specific invoice analysis by ID."""
        result = self.collection.get(
            ids=[invoice_id]
        )
        
        if not result['metadatas']:
            raise ValueError(f"No analysis found for invoice ID: {invoice_id}")
        metadata = result['metadatas'][0]
        # Parse JSON string fields back to Python objects
        for key, value in metadata.items():
            if isinstance(value, str):
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, (list, dict)):
                        metadata[key] = parsed
                except (json.JSONDecodeError, TypeError):
                    pass
        return InvoiceAnalysis(**metadata) 