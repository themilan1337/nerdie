"""
Authentication Router module.
REST API endpoints for Google Firebase authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any

from ..services import auth_service
from ..core import firebase_client
from ..core.firebase_client import FirebaseAuthError


# Security scheme
security = HTTPBearer()

# Router instance
router = APIRouter(prefix="/auth", tags=["Authentication"])


# ============ Request/Response Models ============

class GoogleAuthRequest(BaseModel):
    """Request model for Google OAuth authentication."""
    idToken: str


class AuthResponse(BaseModel):
    """Response model for authentication operations."""
    uid: str
    email: Optional[str]
    displayName: Optional[str]
    photoUrl: Optional[str]
    idToken: str
    refreshToken: str
    expiresIn: str


class UserResponse(BaseModel):
    """Response model for current user info."""
    uid: str
    email: Optional[str]
    emailVerified: bool
    displayName: Optional[str]
    photoUrl: Optional[str]
    disabled: bool
    customClaims: Dict[str, Any]


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    message: str


# ============ Dependencies ============

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency to validate Firebase token and get current user.
    
    Args:
        credentials: HTTP Bearer token from Authorization header
        
    Returns:
        Decoded token claims
        
    Raises:
        HTTPException: 401 if token is invalid or expired
    """
    try:
        token = credentials.credentials
        decoded_token = firebase_client.verify_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "InvalidToken",
                "message": str(e)
            },
            headers={"WWW-Authenticate": "Bearer"}
        )


# ============ Endpoints ============

@router.post(
    "/google",
    response_model=AuthResponse,
    responses={
        401: {"model": ErrorResponse},
        400: {"model": ErrorResponse}
    },
    summary="Authenticate with Google",
    description="Authenticate user with Google OAuth ID token from Firebase"
)
async def google_auth(request: GoogleAuthRequest):
    """
    Authenticate user with Google OAuth.

    Client should:
    1. Use Firebase Auth SDK to sign in with Google (signInWithPopup/signInWithRedirect)
    2. Get the ID token from Firebase Auth
    3. Send the ID token to this endpoint

    Returns uid, email, displayName, photoUrl, and new tokens.
    """
    try:
        result = await auth_service.authenticate_with_google(
            id_token=request.idToken
        )
        return result
    except FirebaseAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": e.error_code,
                "message": e.message
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "AuthError",
                "message": str(e)
            }
        )


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        401: {"model": ErrorResponse}
    },
    summary="Get current user",
    description="Get information about the currently authenticated user"
)
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get current user information.
    
    Requires valid Bearer token in Authorization header.
    Returns uid, email, custom claims, and other user details.
    """
    try:
        user_info = auth_service.get_current_user_info(current_user)
        return user_info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )


@router.get(
    "/health",
    summary="Health check",
    description="Check if the auth service is running"
)
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "auth"}
