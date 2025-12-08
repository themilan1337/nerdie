from firebase_admin import storage
from fastapi import UploadFile
import uuid
from ..core.config import get_settings

settings = get_settings()

class StorageService:
    def __init__(self):
        self._bucket = None
    
    @property
    def bucket(self):
        """Lazy initialization of Firebase Storage bucket."""
        if self._bucket is None:
            self._bucket = storage.bucket()
        return self._bucket

    async def upload_file(self, file: UploadFile, folder: str = "uploads") -> str:
        """
        Upload a file to Firebase Storage.
        Returns the public URL or path.
        """
        # Generate unique filename
        extension = file.filename.split(".")[-1]
        filename = f"{folder}/{uuid.uuid4()}.{extension}"
        
        blob = self.bucket.blob(filename)
        
        # Upload file content
        content = await file.read()
        blob.upload_from_string(
            content,
            content_type=file.content_type
        )
        
        # Make public (optional, depending on requirements)
        # blob.make_public()
        
        return blob.public_url

storage_service = StorageService()

