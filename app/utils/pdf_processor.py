from pypdf import PdfReader
from io import BytesIO
from typing import Union

def extract_text_from_pdf(pdf_content: Union[bytes, BytesIO]) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_content: PDF file content as bytes or BytesIO object
        
    Returns:
        str: Extracted text content
    """
    try:
        # Convert bytes to BytesIO if necessary
        if isinstance(pdf_content, bytes):
            pdf_content = BytesIO(pdf_content)
        
        # Create PDF reader
        pdf_reader = PdfReader(pdf_content)
        
        # Extract text from all pages
        text_content = []
        for page in pdf_reader.pages:
            text_content.append(page.extract_text())
        
        return "\n".join(text_content)
    
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}") 