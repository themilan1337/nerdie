import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from ingestion.app.main import app

client = TestClient(app)

@pytest.fixture
def mock_services(mocker):
    # Mock all services used in ingest.py
    mock_embedding = mocker.patch("ingestion.app.routers.ingest.embedding_service")
    mock_storage = mocker.patch("ingestion.app.routers.ingest.storage_service")
    mock_processing = mocker.patch("ingestion.app.routers.ingest.processing_service")
    mock_graph = mocker.patch("ingestion.app.routers.ingest.graph_extraction_service")
    mock_firestore = mocker.patch("ingestion.app.routers.ingest.firestore_service")
    mock_rag = mocker.patch("ingestion.app.routers.ingest.rag_client")
    
    # Setup default async return values
    mock_embedding.generate_embedding = AsyncMock(return_value=[0.1] * 768)
    mock_embedding.chunk_text = MagicMock(return_value=["chunk1", "chunk2"])
    
    mock_storage.upload_file = AsyncMock(return_value="https://mock-storage.com/file.pdf")
    
    mock_processing.extract_text_from_pdf = AsyncMock(return_value="Mock PDF text content")
    mock_processing.extract_text_from_image = AsyncMock(return_value="Mock Image text content")
    mock_processing.summarize_text = AsyncMock(return_value="Mock summary")
    
    mock_graph.extract_from_chunks = AsyncMock(return_value={"entities": ["e1"], "relations": []})
    
    mock_firestore.save_entities = AsyncMock()
    mock_firestore.save_relations = AsyncMock()
    mock_firestore.save_document_metadata = AsyncMock()
    
    mock_rag.insert_chunk = AsyncMock(return_value={"status": "success"})
    
    return {
        "embedding": mock_embedding,
        "storage": mock_storage,
        "processing": mock_processing,
        "graph": mock_graph,
        "firestore": mock_firestore,
        "rag": mock_rag
    }

def test_ingest_text(mock_services, mock_firebase, real_id_token):
    response = client.post(
        "/ingest/text",
        json={"text": "This is a test text.", "metadata": {"source": "test"}},
        headers={"Authorization": f"Bearer {real_id_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # Verify service calls
    mock_services["embedding"].chunk_text.assert_called()
    mock_services["rag"].insert_chunk.assert_called()
    mock_services["graph"].extract_from_chunks.assert_called()
    mock_services["firestore"].save_entities.assert_called()

def test_ingest_pdf(mock_services, mock_firebase, real_id_token):
    # Create a mock file
    files = {"file": ("test.pdf", b"pdf_content", "application/pdf")}
    
    response = client.post(
        "/ingest/pdf",
        files=files,
        headers={"Authorization": f"Bearer {real_id_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["file_url"] == "https://mock-storage.com/file.pdf"
    
    # Verify service calls
    mock_services["storage"].upload_file.assert_called()
    mock_services["processing"].extract_text_from_pdf.assert_called()
    mock_services["processing"].summarize_text.assert_called() # Verify summarization
    mock_services["firestore"].save_document_metadata.assert_called()

def test_ingest_image(mock_services, mock_firebase, real_id_token):
    # Create a mock file
    files = {"file": ("test.png", b"image_content", "image/png")}
    
    response = client.post(
        "/ingest/image",
        files=files,
        headers={"Authorization": f"Bearer {real_id_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # Verify service calls
    mock_services["storage"].upload_file.assert_called()
    mock_services["processing"].extract_text_from_image.assert_called()
    mock_services["rag"].insert_chunk.assert_called()
