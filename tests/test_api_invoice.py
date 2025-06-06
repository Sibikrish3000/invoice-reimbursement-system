import os
from unittest.mock import patch
from app.api.models.invoice import InvoiceAnalysis, ReimbursementStatus
from datetime import datetime

def test_analyze_invoice_success(client):
    test_dir = os.path.join(os.path.dirname(__file__), "test_files")
    pdf_path = os.path.join(test_dir, "sample.pdf")
    zip_path = os.path.join(test_dir, "invoices.zip")

    # Check PDF validity
    from app.utils.pdf_processor import extract_text_from_pdf
    with open(pdf_path, "rb") as pdf_file:
        try:
            text = extract_text_from_pdf(pdf_file.read())
            print("Extracted text from sample.pdf:", text)
        except Exception as e:
            print("PDF extraction failed:", e)
            assert False, "sample.pdf is not a valid PDF"

    # Check ZIP contents
    import zipfile
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in zf.namelist():
            with zf.open(name) as f:
                try:
                    text = extract_text_from_pdf(f.read())
                    print(f"Extracted text from {name} in zip:", text)
                except Exception as e:
                    print(f"PDF extraction failed for {name} in zip:", e)
                    assert False, f"{name} in invoices.zip is not a valid PDF"

    with open(pdf_path, "rb") as pdf_file, open(zip_path, "rb") as zip_file:
        data = {
            "employee_name": (None, "Test User"),
            "policy_file": ("sample.pdf", pdf_file, "application/pdf"),
            "invoice_files": ("invoices.zip", zip_file, "application/zip"),
        }
        with patch("app.services.invoice_processor.InvoiceProcessor.analyze_invoice") as mock_analyze:
            mock_analyze.return_value = InvoiceAnalysis(
                invoice_id="1",
                employee_name="Test User",
                invoice_date=datetime.fromisoformat("2024-01-01T00:00:00+00:00"),
                total_amount=100.0,
                reimbursable_amount=80.0,
                status=ReimbursementStatus.PARTIALLY_REIMBURSED,
                reason="Test reason",
                policy_violations=[],
                created_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00")
            )
            with patch("app.services.vector_store.VectorStore.store_analysis") as mock_store:
                response = client.post("/api/v1/analyze-invoice", files=data)
                assert response.status_code == 200
                assert response.json()["success"] is True 