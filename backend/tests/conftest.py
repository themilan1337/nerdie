import pytest
from unittest.mock import MagicMock, AsyncMock
import sys
import os

# Add backend directories to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../auth")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../ingestion")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../rag_service")))

@pytest.fixture
def mock_auth_user():
    return "28fjZnSqwENHdUy0HrLEZVTvgvF2"

@pytest.fixture
def real_id_token():
    return "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk1MTg5MTkxMTA3NjA1NDM0NGUxNWUyNTY0MjViYjQyNWVlYjNhNWMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQml6aGFuIEFzaHlraGF0b3YiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSUQzV0dOOHdhV3A3eWQ4cHlCcWhWMTRqbFNkbjk4YnBJakEzbEhLN0hFQzlQZHQ5SWg9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbmVyZGllLTg1ZDBhIiwiYXVkIjoibmVyZGllLTg1ZDBhIiwiYXV0aF90aW1lIjoxNzY1MjEwMTY5LCJ1c2VyX2lkIjoiMjhmalpuU3F3RU5IZFV5T0hyTEVaVlR2Z3ZGMiIsInN1YiI6IjI4ZmpablNxd0VOSGRVeU9IckxFWlZUdmd2RjIiLCJpYXQiOjE3NjUyMTAxNjksImV4cCI6MTc2NTIxMzc2OSwiZW1haWwiOiJiaXpoYW5hc2hAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDc0ODM3OTQ3ODYzMDY1MDAwOTYiXSwiZW1haWwiOlsiYml6aGFuYXNoQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6ImN1c3RvbSJ9fQ.oGZZhne_Vsnb_BurD3Rhj2B1pY7JxCrz2a3xSYVedRE1SLE5VD3_055uQeqJAOQEYrKRby2AyzzwoNiPN92HQAedV78TyXx6U9oxcQrDYz9tcMLNnBN_yBSdaRhoGpnIYtEhTK0a5EmaKFfbSDpg6Sjv0fH3SM_H_MPL1vjZZUwT12JWy5ykibVSt7hhb9cVmP48lMijEjxH7pNW6dCNBC1bYPEJL5f3Q9ykuYcAjlM-8DMleh-Tyhh2lGWHLTNHrAeijnyINSIlp5BnACFpBSHuoqfgla3HgQIYg1NEQ3a5f6ghJQ5jjF-kxVv7dXMdkLQreQnmQBzp7B1zqD0zIA"

@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.commit = MagicMock()
    session.rollback = MagicMock()
    session.refresh = MagicMock()
    session.add = MagicMock()
    session.query = MagicMock()
    return session

@pytest.fixture
def mock_gemini(mocker):
    mock_genai = mocker.patch("google.generativeai.GenerativeModel")
    mock_model = MagicMock()
    mock_genai.return_value = mock_model
    
    # Mock generate_content
    mock_response = MagicMock()
    mock_response.text = "This is a mock Gemini response."
    mock_model.generate_content.return_value = mock_response
    
    # Mock embed_content
    mocker.patch("google.generativeai.embed_content", return_value={"embedding": [0.1] * 768})
    
    return mock_genai

@pytest.fixture
def mock_firebase(mocker):
    mock_auth = mocker.patch("firebase_admin.auth")
    mock_storage = mocker.patch("firebase_admin.storage")
    mock_firestore = mocker.patch("firebase_admin.firestore")
    
    # Mock verify_id_token
    mock_auth.verify_id_token.return_value = {"uid": "28fjZnSqwENHdUy0HrLEZVTvgvF2"}
    
    # Mock storage bucket
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_blob.public_url = "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf"
    mock_bucket.blob.return_value = mock_blob
    mock_storage.bucket.return_value = mock_bucket
    
    return mock_auth, mock_storage, mock_firestore
