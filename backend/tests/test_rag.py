import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from rag_service.app.main import app
from rag_service.app.models.chunk import DocumentChunk
from uuid import uuid4
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def mock_rag_services(mocker):
    # Mock gemini client
    mock_gemini = mocker.patch("rag_service.app.services.rag_service.gemini_client")
    mock_gemini.generate_query_embedding = AsyncMock(return_value=[0.1] * 768)
    mock_gemini.generate_answer = AsyncMock(return_value="This is a mock answer.")
    
    # Mock similarity search
    mock_search = mocker.patch("rag_service.app.services.rag_service.similarity_search")
    
    # Create mock chunks
    chunk1 = DocumentChunk(
        id=uuid4(),
        user_id="28fjZnSqwENHdUy0HrLEZVTvgvF2",
        text="Chunk 1 text",
        metadata={"source": "doc1.pdf"},
        created_at=datetime.utcnow()
    )
    chunk2 = DocumentChunk(
        id=uuid4(),
        user_id="28fjZnSqwENHdUy0HrLEZVTvgvF2",
        text="Chunk 2 text",
        metadata={"source": "doc2.pdf"},
        created_at=datetime.utcnow()
    )
    
    mock_search.return_value = [(chunk1, 0.1), (chunk2, 0.2)]
    
    # Mock vector service for insert
    mock_vector = mocker.patch("rag_service.app.api.vector.vector_service")
    mock_vector.insert_chunk = AsyncMock(return_value=chunk1)
    
    return {
        "gemini": mock_gemini,
        "search": mock_search,
        "vector": mock_vector
    }

def test_rag_query(mock_rag_services, mock_db_session):
    response = client.post(
        "/rag/query",
        json={
            "query": "test question",
            "user_id": "28fjZnSqwENHdUy0HrLEZVTvgvF2",
            "top_k": 3
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This is a mock answer."
    assert len(data["chunks"]) == 2
    assert data["chunks"][0]["text"] == "Chunk 1 text"
    
    # Verify pipeline calls
    mock_rag_services["gemini"].generate_query_embedding.assert_called_with("test question")
    mock_rag_services["search"].assert_called()
    mock_rag_services["gemini"].generate_answer.assert_called()

def test_vector_insert(mock_rag_services, mock_db_session):
    chunk_id = str(uuid4())
    response = client.post(
        "/vector/insert",
        json={
            "id": chunk_id,
            "user_id": "28fjZnSqwENHdUy0HrLEZVTvgvF2",
            "text": "New chunk text",
            "embedding": [0.1] * 768,
            "metadata": {"source": "new_doc.pdf"}
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["id"] == str(mock_rag_services["vector"].insert_chunk.return_value.id)
    
    # Verify service call
    mock_rag_services["vector"].insert_chunk.assert_called()
