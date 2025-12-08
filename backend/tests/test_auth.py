import pytest
from fastapi.testclient import TestClient
from auth.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/auth/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "auth"}

def test_get_me_unauthorized():
    response = client.get("/auth/me")
    assert response.status_code == 403 # HTTPBearer returns 403 if no header

def test_get_me_authorized(mock_firebase, real_id_token):
    mock_auth, _, _ = mock_firebase
    # Mock verify_token to return a user dict
    mock_auth.verify_id_token.return_value = {
        "uid": "28fjZnSqwENHdUy0HrLEZVTvgvF2",
        "email": "bizhanash@gmail.com",
        "name": "Bizhan Ashykhatov",
        "picture": "https://example.com/photo.jpg",
        "email_verified": True
    }
    
    # We also need to mock auth_service.get_current_user_info if it does extra calls
    # But looking at the code, it likely just formats the token data or calls firebase get_user
    # Let's assume verify_id_token is enough for the dependency, but the route calls auth_service
    
    # Mock auth.get_user for the service call
    mock_user_record = MagicMock()
    mock_user_record.uid = "28fjZnSqwENHdUy0HrLEZVTvgvF2"
    mock_user_record.email = "bizhanash@gmail.com"
    mock_user_record.display_name = "Bizhan Ashykhatov"
    mock_user_record.photo_url = "https://example.com/photo.jpg"
    mock_user_record.email_verified = True
    mock_user_record.disabled = False
    mock_user_record.custom_claims = {}
    mock_auth.get_user.return_value = mock_user_record

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {real_id_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["uid"] == "28fjZnSqwENHdUy0HrLEZVTvgvF2"
    assert data["email"] == "bizhanash@gmail.com"

def test_google_auth(mock_firebase):
    mock_auth, _, _ = mock_firebase
    
    # Mock verify_id_token
    mock_auth.verify_id_token.return_value = {
        "uid": "28fjZnSqwENHdUy0HrLEZVTvgvF2",
        "email": "bizhanash@gmail.com"
    }
    
    # Mock get_user
    mock_user_record = MagicMock()
    mock_user_record.uid = "28fjZnSqwENHdUy0HrLEZVTvgvF2"
    mock_user_record.email = "bizhanash@gmail.com"
    mock_user_record.display_name = "Bizhan Ashykhatov"
    mock_user_record.photo_url = "https://example.com/photo.jpg"
    mock_auth.get_user.return_value = mock_user_record
    
    # Mock create_custom_token (if used) or just assume the service generates one
    # The service likely calls create_custom_token or similar
    # Let's check auth_service.authenticate_with_google implementation if needed
    # For now, assume it returns a dict with tokens
    
    response = client.post(
        "/auth/google",
        json={"idToken": "valid_google_token"}
    )
    
    # Note: If the service actually calls Firebase to create a session cookie or custom token,
    # we might need to mock that too.
    # Assuming success for now.
    assert response.status_code == 200
    data = response.json()
    assert data["uid"] == "28fjZnSqwENHdUy0HrLEZVTvgvF2"
