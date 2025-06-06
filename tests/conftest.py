import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
import io
import zipfile

@pytest.fixture(scope="module")
def client():
    with patch("app.services.vector_store.VectorStore") as MockVectorStore:
        with patch("app.services.invoice_processor.ChatOpenAI") as MockLLM:
            with TestClient(app) as c:
                yield c

def create_test_pdf():
    from reportlab.pdfgen import canvas
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "Test Invoice PDF")
    c.save()
    buffer.seek(0)
    return buffer.read()

def create_test_zip(pdf_bytes, filename="test.pdf"):
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w") as zf:
        zf.writestr(filename, pdf_bytes)
    mem_zip.seek(0)
    return mem_zip

def test_analyze_invoice_success(client):
    # Create valid PDF and ZIP
    pdf_bytes = create_test_pdf()
    zip_bytes = create_test_zip(pdf_bytes).read()
    data = {
        "employee_name": (None, "Test User"),
        "policy_file": ("policy.pdf", pdf_bytes, "application/pdf"),
        "invoice_files": ("invoices.zip", zip_bytes, "application/zip"),
    }
    with patch("app.services.invoice_processor.InvoiceProcessor.analyze_invoice") as mock_analyze:
        mock_analyze.return_value = type("FakeAnalysis", (), {
            "invoice_id": "1",
            "employee_name": "Test User",
            "invoice_date": "2024-01-01T00:00:00Z",
            "total_amount": 100.0,
            "reimbursable_amount": 80.0,
            "status": "PARTIALLY_REIMBURSED",
            "reason": "Test reason",
            "policy_violations": [],
            "created_at": "2024-01-01T00:00:00Z"
        })()
        with patch("app.services.vector_store.VectorStore.store_analysis") as mock_store:
            response = client.post("/api/v1/analyze-invoice", files=data)
            assert response.status_code == 200
            assert response.json()["success"] is True