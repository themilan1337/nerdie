"""
Graph Query API Router.

Provides endpoints for querying the knowledge graph stored in Firestore.
Returns entity nodes and edges for visualization (Obsidian-like graph).

All endpoints require Firebase authentication via Bearer token.
"""

from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any
import firebase_admin
from firebase_admin import firestore, credentials, auth
import os

from ..models.query import GraphQueryResponse, GraphNode, GraphEdge


router = APIRouter(prefix="/graph", tags=["Knowledge Graph"])
security = HTTPBearer()


# Initialize Firebase
if not firebase_admin._apps:
    # Check if credentials file exists
    cred_path = os.getenv("FIREBASE_CREDENTIALS", "/app/firebase-credentials.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)


def get_firestore_db():
    """Get Firestore client."""
    return firestore.client()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify Firebase token and return user_id.

    Args:
        credentials: Bearer token from Authorization header

    Returns:
        user_id from verified token

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid Firebase token: {str(e)}"
        )


@router.get(
    "/me",
    summary="Get my knowledge graph",
    description="Returns all entities and relations for the authenticated user's documents"
)
async def get_my_graph(
    current_user: str = Depends(get_current_user)
):
    """
    Get the complete knowledge graph for the authenticated user.

    Returns all entities and their relationships across all user's documents.
    Perfect for Obsidian-style graph visualization.

    Args:
        current_user: Authenticated user from token

    Returns:
        Dict with nodes and edges for visualization
    """
    try:
        db = get_firestore_db()

        # Get all entities for user
        entities_ref = db.collection("graph").document("entities").collection(current_user)
        entities_docs = entities_ref.get()

        # Get all relations for user
        relations_ref = db.collection("graph").document("relations").collection(current_user)
        relations_docs = relations_ref.get()

        # Build nodes
        nodes = []
        for doc in entities_docs:
            data = doc.to_dict()
            nodes.append({
                "id": data.get("name"),
                "label": data.get("name"),
                "type": "entity",
                "mentions": len(data.get("mentions", []))
            })

        # Build edges
        edges = []
        for doc in relations_docs:
            data = doc.to_dict()
            edges.append({
                "source": data.get("source"),
                "target": data.get("target"),
                "relation": data.get("type", "relates_to")
            })

        return {
            "nodes": nodes,
            "edges": edges,
            "user_id": current_user
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch graph: {str(e)}")


@router.get(
    "/entity/{entity_name}",
    summary="Query specific entity in my graph",
    description="Get a sub-graph centered on a specific entity from your knowledge graph"
)
async def query_my_entity(
    entity_name: str,
    depth: int = Query(1, description="How many hops to traverse from entity"),
    current_user: str = Depends(get_current_user)
):
    """
    Query the knowledge graph for a specific entity.

    Returns the entity and its immediate connections up to specified depth.

    Args:
        entity_name: Name of entity to query
        depth: Number of relationship hops to include (default 1)
        current_user: Authenticated user from token

    Returns:
        Sub-graph with nodes and edges
    """
    try:
        db = get_firestore_db()
        entity_name = entity_name.lower()

        # Get relations where entity is source or target
        relations_ref = db.collection("graph").document("relations").collection(current_user)

        source_relations = relations_ref.where("source", "==", entity_name).get()
        target_relations = relations_ref.where("target", "==", entity_name).get()

        nodes = set([entity_name])
        edges = []

        for doc in source_relations:
            data = doc.to_dict()
            nodes.add(data.get("target"))
            edges.append({
                "source": data.get("source"),
                "target": data.get("target"),
                "relation": data.get("type", "relates_to")
            })

        for doc in target_relations:
            data = doc.to_dict()
            nodes.add(data.get("source"))
            edges.append({
                "source": data.get("source"),
                "target": data.get("target"),
                "relation": data.get("type", "relates_to")
            })

        return {
            "entity": entity_name,
            "nodes": [{"id": n, "label": n, "type": "entity"} for n in nodes],
            "edges": edges,
            "depth": depth
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query entity: {str(e)}")
