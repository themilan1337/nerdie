"""
Graph Query API Router.

MVP endpoint for knowledge graph queries.
Returns entity nodes and edges from the knowledge graph.

Currently a stub - will be populated by ingestion service.
"""

from fastapi import APIRouter, Query

from ..models.query import GraphQueryResponse, GraphNode, GraphEdge


router = APIRouter(prefix="/graph", tags=["Knowledge Graph"])


@router.get(
    "/query",
    response_model=GraphQueryResponse,
    summary="Query knowledge graph (MVP)",
    description="Query the knowledge graph for entity relationships. Currently returns stub data."
)
async def graph_query(
    entity: str = Query(..., description="Entity name to query")
):
    """
    Query the knowledge graph for an entity.
    
    MVP Implementation:
    - Returns empty nodes and edges
    - Will be populated by ingestion service after entity extraction
    
    Future implementation will:
    1. Search for entity in Firestore graph collection
    2. Return connected nodes and edges
    3. Support depth parameter for traversal
    """
    # MVP stub response
    return GraphQueryResponse(
        entity=entity,
        nodes=[],
        edges=[]
    )
