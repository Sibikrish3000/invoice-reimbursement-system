from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.api.models.invoice import InvoiceAnalysisRequest, InvoiceAnalysisResponse
from app.services.invoice_processor import InvoiceProcessor
from app.services.vector_store import VectorStore
from app.utils.pdf_processor import extract_text_from_pdf
import zipfile
import io
from typing import List

router = APIRouter()
invoice_processor = InvoiceProcessor()
vector_store = VectorStore()

@router.post("/analyze-invoice", response_model=InvoiceAnalysisResponse)
async def analyze_invoice(
    policy_file: UploadFile = File(...),
    invoice_files: UploadFile = File(...),
    employee_name: str = Form(...)
):
    try:
        # Read and process policy file
        policy_content = await policy_file.read()
        policy_text = extract_text_from_pdf(policy_content)
        
        # Process invoice files (ZIP)
        invoice_analyses = []
        with zipfile.ZipFile(io.BytesIO(await invoice_files.read())) as zip_ref:
            for filename in zip_ref.namelist():
                if filename.endswith('.pdf'):
                    # Extract and process each PDF
                    with zip_ref.open(filename) as pdf_file:
                        invoice_text = extract_text_from_pdf(pdf_file.read())
                        
                        # Analyze invoice
                        analysis = await invoice_processor.analyze_invoice(
                            employee_name=employee_name,
                            policy_text=policy_text,
                            invoice_text=invoice_text
                        )
                        
                        # Store in vector database
                        vector_store.store_analysis(analysis)
                        invoice_analyses.append(analysis)
        
        return InvoiceAnalysisResponse(
            success=True,
            message=f"Successfully analyzed {len(invoice_analyses)} invoices",
            analysis=invoice_analyses[0] if invoice_analyses else None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing invoices: {str(e)}"
        ) 