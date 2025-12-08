import io
from pypdf import PdfReader
from fastapi import UploadFile
import google.generativeai as genai
from PIL import Image
from ..core.config import get_settings

settings = get_settings()

class ProcessingService:
    def __init__(self):
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')

    async def extract_text_from_pdf(self, file: UploadFile) -> str:
        """Extract text from uploaded PDF file."""
        content = await file.read()
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        # Reset file cursor for subsequent operations if needed
        await file.seek(0)
        return text

    async def extract_text_from_image(self, file: UploadFile) -> str:
        """Extract text from image using Gemini Vision."""
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        
        response = self.vision_model.generate_content(
            ["Extract all text from this image.", image]
        )
        
        # Reset file cursor
        await file.seek(0)
        return response.text

processing_service = ProcessingService()
