"""
Authentication Service module.
Business logic layer for Google Firebase authentication.
"""

from typing import Dict, Any
from ..core import firebase_client
from ..core.firebase_client import FirebaseAuthError


async def authenticate_with_google(id_token: str) -> Dict[str, Any]:
    """
    Authenticate user with Google OAuth via Firebase.

    Args:
        id_token: Firebase ID token obtained after Google sign-in on client

    Returns:
        Dict containing uid, email, displayName, photoUrl, idToken, refreshToken
    """
    result = await firebase_client.verify_and_get_user(id_token)
    return {
        "uid": result["uid"],
        "email": result.get("email"),
        "displayName": result.get("displayName"),
        "photoUrl": result.get("photoUrl"),
        "idToken": result["idToken"],
        "refreshToken": result["refreshToken"],
        "expiresIn": result["expiresIn"]
    }


def get_current_user_info(decoded_token: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract user info from decoded Firebase token.
    
    Args:
        decoded_token: Decoded Firebase ID token claims
        
    Returns:
        Dict containing uid, email, custom claims
    """
    # Get user record for additional info
    user_record = firebase_client.get_user(decoded_token["uid"])
    
    # Extract custom claims (if any)
    custom_claims = decoded_token.get("claims", {})
    
    # Filter out standard claims to get custom ones
    standard_claims = {
        "iss", "aud", "auth_time", "user_id", "sub", "iat", "exp",
        "email", "email_verified", "firebase", "uid"
    }
    custom_claims = {
        k: v for k, v in decoded_token.items() 
        if k not in standard_claims
    }
    
    return {
        "uid": decoded_token["uid"],
        "email": decoded_token.get("email"),
        "emailVerified": decoded_token.get("email_verified", False),
        "displayName": user_record.display_name,
        "photoUrl": user_record.photo_url,
        "disabled": user_record.disabled,
        "customClaims": custom_claims
    }
