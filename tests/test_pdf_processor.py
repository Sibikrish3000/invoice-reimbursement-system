import pytest
from app.utils.pdf_processor import extract_text_from_pdf
from io import BytesIO

def test_extract_text_from_pdf():
    try:
        from reportlab.pdfgen import canvas
    except ImportError:
        pytest.skip("reportlab not installed")
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, "Hello PDF")
    c.save()
    buffer.seek(0)
    pdf_bytes = buffer.read()
    text = extract_text_from_pdf(pdf_bytes)
    assert "Hello PDF" in text 