import io
from pypdf import PdfReader
from fastapi import UploadFile
import google.generativeai as genai
from PIL import Image
from ..core.config import get_settings

settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class ProcessingService:
    def __init__(self):
        # Use gemini-2.5-flash for vision (gemini-pro-vision is deprecated)
        self.vision_model = genai.GenerativeModel('gemini-2.5-flash')

    async def extract_text_from_pdf(self, file: UploadFile) -> str:
        """Extract text from uploaded PDF file."""
        content = await file.read()
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            
        # Reset file cursor for subsequent operations if needed
        await file.seek(0)
        return text

    async def extract_text_from_image(self, file: UploadFile) -> str:
        """Extract text from image using Gemini Vision."""
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        
        response = self.vision_model.generate_content(
            [
                "Extract all text from this image. If there is no text, describe what you see in detail.",
                image
            ]
        )
        
        # Reset file cursor
        await file.seek(0)
        return response.text if response.text else ""

    async def summarize_text(self, text: str) -> str:
        """
        Generate a brief summary of the text using Gemini.
        
        Args:
            text: Input text to summarize
            
        Returns:
            Summary string
        """
        try:
            # Truncate text if too long to avoid token limits (approx 10k chars is safe for flash)
            truncated_text = text[:30000]
            
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(
                f"Please provide a concise 2-3 sentence summary of the following document:\n\n{truncated_text}"
            )
            
            return response.text if response.text else "No summary available."
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Summary generation failed."

processing_service = ProcessingService()

