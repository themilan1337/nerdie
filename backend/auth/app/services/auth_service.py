"""
Authentication Service module.
Business logic layer for authentication operations.
"""

from typing import Dict, Any
from ..core import firebase_client
from ..core.firebase_client import FirebaseAuthError


async def signup_user(email: str, password: str) -> Dict[str, Any]:
    """
    Create a new user account.
    
    Args:
        email: User email address
        password: User password
        
    Returns:
        Dict containing uid, email, idToken, refreshToken
    """
    result = await firebase_client.create_user(email, password)
    return {
        "uid": result["uid"],
        "email": result["email"],
        "idToken": result["idToken"],
        "refreshToken": result["refreshToken"],
        "expiresIn": result["expiresIn"]
    }


async def login_user(email: str, password: str) -> Dict[str, Any]:
    """
    Authenticate user with email and password.
    
    Args:
        email: User email address
        password: User password
        
    Returns:
        Dict containing idToken, refreshToken, uid, email
    """
    result = await firebase_client.sign_in(email, password)
    return {
        "uid": result["uid"],
        "email": result["email"],
        "idToken": result["idToken"],
        "refreshToken": result["refreshToken"],
        "expiresIn": result["expiresIn"]
    }


async def refresh_user_token(refresh_token: str) -> Dict[str, Any]:
    """
    Refresh user's ID token using refresh token.
    
    Args:
        refresh_token: Firebase refresh token
        
    Returns:
        Dict containing new idToken, refreshToken, uid
    """
    result = await firebase_client.refresh_token(refresh_token)
    return {
        "uid": result["uid"],
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
