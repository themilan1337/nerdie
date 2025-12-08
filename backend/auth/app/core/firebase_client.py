"""
Firebase Client module.
Handles Firebase Admin SDK initialization and authentication operations.
"""

import json
import firebase_admin
from firebase_admin import credentials, auth
import httpx
from typing import Optional, Dict, Any
from .config import get_settings


# Global Firebase app instance
_firebase_app: Optional[firebase_admin.App] = None


def initialize_firebase() -> firebase_admin.App:
    """
    Initialize Firebase Admin SDK.
    Returns existing app if already initialized.
    """
    global _firebase_app
    
    if _firebase_app is not None:
        return _firebase_app
    
    settings = get_settings()
    
    # Load credentials from file or JSON string
    cred_path = settings.firebase_credentials
    
    if cred_path.startswith("{"):
        # JSON string provided directly
        cred_dict = json.loads(cred_path)
        cred = credentials.Certificate(cred_dict)
    else:
        # File path provided
        cred = credentials.Certificate(cred_path)
    
    _firebase_app = firebase_admin.initialize_app(cred, {
        'projectId': settings.firebase_project_id
    })
    
    return _firebase_app


def verify_token(id_token: str) -> Dict[str, Any]:
    """
    Verify Firebase ID token using Admin SDK.
    
    Args:
        id_token: Firebase ID token to verify
        
    Returns:
        Decoded token claims
        
    Raises:
        firebase_admin.auth.InvalidIdTokenError: If token is invalid
        firebase_admin.auth.ExpiredIdTokenError: If token is expired
    """
    return auth.verify_id_token(id_token)


def get_user(uid: str) -> auth.UserRecord:
    """
    Get user record by UID.
    
    Args:
        uid: Firebase user UID
        
    Returns:
        UserRecord object
    """
    return auth.get_user(uid)


async def create_user(email: str, password: str) -> Dict[str, Any]:
    """
    Create a new user in Firebase Auth via REST API.
    Returns user data including idToken.
    
    Args:
        email: User email
        password: User password
        
    Returns:
        Dict containing uid, email, idToken, refreshToken
    """
    settings = get_settings()
    
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={settings.firebase_api_key}"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
        )
        
        data = response.json()
        
        if response.status_code != 200:
            error_message = data.get("error", {}).get("message", "Unknown error")
            raise FirebaseAuthError(error_message)
        
        return {
            "uid": data.get("localId"),
            "email": data.get("email"),
            "idToken": data.get("idToken"),
            "refreshToken": data.get("refreshToken"),
            "expiresIn": data.get("expiresIn")
        }


async def sign_in(email: str, password: str) -> Dict[str, Any]:
    """
    Sign in user with email and password via Firebase REST API.
    
    Args:
        email: User email
        password: User password
        
    Returns:
        Dict containing idToken, refreshToken, uid, email
    """
    settings = get_settings()
    
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.firebase_api_key}"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
        )
        
        data = response.json()
        
        if response.status_code != 200:
            error_message = data.get("error", {}).get("message", "Unknown error")
            raise FirebaseAuthError(error_message)
        
        return {
            "uid": data.get("localId"),
            "email": data.get("email"),
            "idToken": data.get("idToken"),
            "refreshToken": data.get("refreshToken"),
            "expiresIn": data.get("expiresIn")
        }


async def refresh_token(refresh_token: str) -> Dict[str, Any]:
    """
    Refresh ID token using refresh token via Firebase REST API.
    
    Args:
        refresh_token: Firebase refresh token
        
    Returns:
        Dict containing new idToken, refreshToken, uid
    """
    settings = get_settings()
    
    url = f"https://securetoken.googleapis.com/v1/token?key={settings.firebase_api_key}"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }
        )
        
        data = response.json()
        
        if response.status_code != 200:
            error_message = data.get("error", {}).get("message", "Unknown error")
            raise FirebaseAuthError(error_message)
        
        return {
            "uid": data.get("user_id"),
            "idToken": data.get("id_token"),
            "refreshToken": data.get("refresh_token"),
            "expiresIn": data.get("expires_in")
        }


class FirebaseAuthError(Exception):
    """Custom exception for Firebase authentication errors."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
    
    @property
    def error_code(self) -> str:
        """Map Firebase error messages to error codes."""
        error_mapping = {
            "EMAIL_EXISTS": "EmailAlreadyExists",
            "EMAIL_NOT_FOUND": "InvalidCredentials",
            "INVALID_PASSWORD": "InvalidCredentials",
            "INVALID_LOGIN_CREDENTIALS": "InvalidCredentials",
            "USER_DISABLED": "UserDisabled",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "TooManyAttempts",
            "WEAK_PASSWORD": "WeakPassword",
            "INVALID_EMAIL": "InvalidEmail",
            "TOKEN_EXPIRED": "TokenExpired",
            "INVALID_REFRESH_TOKEN": "InvalidRefreshToken",
        }
        return error_mapping.get(self.message, "AuthError")
