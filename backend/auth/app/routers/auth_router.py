"""
Authentication Router module.
REST API endpoints for authentication operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

from ..services import auth_service
from ..core import firebase_client
from ..core.firebase_client import FirebaseAuthError


# Security scheme
security = HTTPBearer()

# Router instance
router = APIRouter(prefix="/auth", tags=["Authentication"])


# ============ Request/Response Models ============

class SignupRequest(BaseModel):
    """Request model for user signup."""
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Request model for token refresh."""
    refreshToken: str


class AuthResponse(BaseModel):
    """Response model for authentication operations."""
    uid: str
    email: str
    idToken: str
    refreshToken: str
    expiresIn: str


class RefreshResponse(BaseModel):
    """Response model for token refresh."""
    uid: str
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
    "/signup",
    response_model=AuthResponse,
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse}
    },
    summary="Create new user account",
    description="Register a new user with email and password"
)
async def signup(request: SignupRequest):
    """
    Create a new user account in Firebase Auth.
    
    Returns uid, email, idToken, and refreshToken.
    """
    try:
        result = await auth_service.signup_user(
            email=request.email,
            password=request.password
        )
        return result
    except FirebaseAuthError as e:
        status_code = status.HTTP_400_BAD_REQUEST
        if e.error_code == "EmailAlreadyExists":
            status_code = status.HTTP_409_CONFLICT
        
        raise HTTPException(
            status_code=status_code,
            detail={
                "error": e.error_code,
                "message": e.message
            }
        )


@router.post(
    "/login",
    response_model=AuthResponse,
    responses={
        401: {"model": ErrorResponse}
    },
    summary="User login",
    description="Authenticate user with email and password"
)
async def login(request: LoginRequest):
    """
    Authenticate user and return tokens.
    
    Returns idToken, refreshToken, uid, and email.
    """
    try:
        result = await auth_service.login_user(
            email=request.email,
            password=request.password
        )
        return result
    except FirebaseAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": e.error_code,
                "message": "Email or password is incorrect"
            }
        )


@router.post(
    "/refresh",
    response_model=RefreshResponse,
    responses={
        401: {"model": ErrorResponse}
    },
    summary="Refresh access token",
    description="Get a new ID token using refresh token"
)
async def refresh(request: RefreshRequest):
    """
    Refresh the ID token using a refresh token.
    
    Returns new idToken and refreshToken.
    """
    try:
        result = await auth_service.refresh_user_token(
            refresh_token=request.refreshToken
        )
        return result
    except FirebaseAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": e.error_code,
                "message": "Invalid or expired refresh token"
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
