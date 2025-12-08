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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjZTU4..."
                }
            ]
        }
    }


class AuthResponse(BaseModel):
    """Response model for authentication operations."""
    uid: str
    email: Optional[str]
    displayName: Optional[str]
    photoUrl: Optional[str]
    idToken: str
    refreshToken: str
    expiresIn: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uid": "abc123def456",
                    "email": "user@gmail.com",
                    "displayName": "John Doe",
                    "photoUrl": "https://lh3.googleusercontent.com/a/...",
                    "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjZTU4...",
                    "refreshToken": "AMf-vBxW8Z...",
                    "expiresIn": "3600"
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """Response model for current user info."""
    uid: str
    email: Optional[str]
    emailVerified: bool
    displayName: Optional[str]
    photoUrl: Optional[str]
    disabled: bool
    customClaims: Dict[str, Any]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uid": "abc123def456",
                    "email": "user@gmail.com",
                    "emailVerified": True,
                    "displayName": "John Doe",
                    "photoUrl": "https://lh3.googleusercontent.com/a/...",
                    "disabled": False,
                    "customClaims": {}
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "InvalidToken",
                    "message": "The provided token is invalid or expired"
                }
            ]
        }
    }


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
        200: {
            "description": "Successful authentication",
            "model": AuthResponse,
            "content": {
                "application/json": {
                    "example": {
                        "uid": "abc123def456",
                        "email": "user@gmail.com",
                        "displayName": "John Doe",
                        "photoUrl": "https://lh3.googleusercontent.com/a/default-user",
                        "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjZTU4...",
                        "refreshToken": "AMf-vBxW8Z1a2b3c4d5e6f7g8h9i...",
                        "expiresIn": "3600"
                    }
                }
            }
        },
        401: {
            "description": "Invalid or expired token",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "error": "InvalidToken",
                        "message": "The provided Firebase ID token is invalid or expired"
                    }
                }
            }
        },
        400: {
            "description": "Bad request",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "error": "AuthError",
                        "message": "Failed to authenticate with Google"
                    }
                }
            }
        }
    },
    summary="🔐 Google OAuth Authentication",
    description="""
    Authenticate user with Google OAuth via Firebase.

    ## How it works:

    ### Frontend (Client-Side):
    ```javascript
    import { initializeApp } from 'firebase/app';
    import { getAuth, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';

    // 1. Initialize Firebase
    const firebaseConfig = {
        apiKey: "YOUR_API_KEY",
        authDomain: "YOUR_PROJECT.firebaseapp.com",
        projectId: "YOUR_PROJECT_ID"
    };
    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);

    // 2. Sign in with Google
    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);

    // 3. Get the ID token
    const idToken = await result.user.getIdToken();

    // 4. Send to your backend
    const response = await fetch('http://your-api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idToken })
    });
    ```

    ### Backend (This Endpoint):
    - Verifies the Firebase ID token
    - Extracts user information (uid, email, name, photo)
    - Generates new tokens for your application
    - Returns user data and tokens

    ## Request Body:
    ```json
    {
        "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjZTU4..."
    }
    ```

    ## Response:
    ```json
    {
        "uid": "abc123def456",
        "email": "user@gmail.com",
        "displayName": "John Doe",
        "photoUrl": "https://lh3.googleusercontent.com/a/...",
        "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjZTU4...",
        "refreshToken": "AMf-vBxW8Z...",
        "expiresIn": "3600"
    }
    ```

    ## Use the returned tokens:
    - Store `idToken` and `refreshToken` securely in your client
    - Use `idToken` in Authorization header: `Bearer {idToken}`
    - Token expires after 3600 seconds (1 hour)
    """
)
async def google_auth(request: GoogleAuthRequest):
    """
    Authenticate user with Google OAuth.

    This endpoint processes Firebase ID tokens obtained after Google sign-in.
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
        200: {
            "description": "Current user information",
            "model": UserResponse,
            "content": {
                "application/json": {
                    "example": {
                        "uid": "abc123def456",
                        "email": "user@gmail.com",
                        "emailVerified": True,
                        "displayName": "John Doe",
                        "photoUrl": "https://lh3.googleusercontent.com/a/default-user",
                        "disabled": False,
                        "customClaims": {"role": "user", "premium": True}
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized - Invalid or missing token",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "error": "InvalidToken",
                        "message": "The provided token is invalid or expired"
                    }
                }
            }
        }
    },
    summary="👤 Get Current User",
    description="""
    Get information about the currently authenticated user.

    ## How to use:

    ### Request:
    ```bash
    curl -X GET 'http://your-api/auth/me' \\
      -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjZTU4...'
    ```

    ### JavaScript example:
    ```javascript
    const response = await fetch('http://your-api/auth/me', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${idToken}`
        }
    });
    const userData = await response.json();
    console.log(userData);
    ```

    ## Response:
    ```json
    {
        "uid": "abc123def456",
        "email": "user@gmail.com",
        "emailVerified": true,
        "displayName": "John Doe",
        "photoUrl": "https://lh3.googleusercontent.com/a/...",
        "disabled": false,
        "customClaims": {}
    }
    ```

    ## Authentication:
    - Requires Bearer token in Authorization header
    - Get the token from `/auth/google` endpoint
    - Token must be valid and not expired
    """
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
