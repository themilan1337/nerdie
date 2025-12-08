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


async def verify_and_get_user(id_token: str) -> Dict[str, Any]:
    """
    Verify Google OAuth ID token and get/create user in Firebase.

    This function:
    1. Verifies the Firebase ID token (which contains Google auth info)
    2. Gets or creates the user in Firebase Auth
    3. Generates custom token for the user
    4. Exchanges custom token for ID token and refresh token

    Args:
        id_token: Firebase ID token from client after Google sign-in

    Returns:
        Dict containing uid, email, displayName, photoUrl, idToken, refreshToken
    """
    try:
        # Verify the ID token
        decoded_token = verify_token(id_token)
        uid = decoded_token["uid"]

        # Get user record
        user_record = get_user(uid)

        # Generate a custom token for this user
        custom_token = auth.create_custom_token(uid)

        # Exchange custom token for ID token and refresh token
        settings = get_settings()
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={settings.firebase_api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json={
                    "token": custom_token.decode("utf-8"),
                    "returnSecureToken": True
                }
            )

            data = response.json()

            if response.status_code != 200:
                error_message = data.get("error", {}).get("message", "Token exchange failed")
                raise FirebaseAuthError(error_message)

            return {
                "uid": uid,
                "email": user_record.email,
                "displayName": user_record.display_name,
                "photoUrl": user_record.photo_url,
                "idToken": data.get("idToken"),
                "refreshToken": data.get("refreshToken"),
                "expiresIn": data.get("expiresIn", "3600")
            }

    except Exception as e:
        raise FirebaseAuthError(str(e))


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
