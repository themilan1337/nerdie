"""
Firestore service for Knowledge Graph storage.

Stores entities and relations in Firebase Firestore.
"""

import uuid
from typing import List, Dict, Any, Optional
import firebase_admin
from firebase_admin import firestore
from datetime import datetime


class FirestoreService:
    def __init__(self):
        self._db = None
    
    @property
    def db(self):
        """Lazy initialization of Firestore client."""
        if self._db is None:
            self._db = firestore.client()
        return self._db
    
    async def save_entities(self, user_id: str, entities: List[str], source_chunk_id: str = None) -> List[str]:
        """
        Save entities to Firestore.
        
        Args:
            user_id: User who owns these entities
            entities: List of entity names
            source_chunk_id: Optional source chunk reference
            
        Returns:
            List of created entity IDs
        """
        entity_ids = []
        entities_ref = self.db.collection("graph").document("entities").collection(user_id)
        
        for entity_name in entities:
            # Check if entity already exists
            existing = entities_ref.where("name", "==", entity_name.lower()).limit(1).get()
            
            if existing:
                # Update mentions
                doc = existing[0]
                doc.reference.update({
                    "mentions": firestore.ArrayUnion([source_chunk_id] if source_chunk_id else []),
                    "updated_at": datetime.utcnow()
                })
                entity_ids.append(doc.id)
            else:
                # Create new entity
                entity_id = str(uuid.uuid4())
                entities_ref.document(entity_id).set({
                    "name": entity_name.lower(),
                    "user_id": user_id,
                    "mentions": [source_chunk_id] if source_chunk_id else [],
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                })
                entity_ids.append(entity_id)
        
        return entity_ids
    
    async def save_relations(self, user_id: str, relations: List[Dict[str, str]]) -> List[str]:
        """
        Save relations to Firestore.
        
        Args:
            user_id: User who owns these relations
            relations: List of relation dicts with source, target, type
            
        Returns:
            List of created relation IDs
        """
        relation_ids = []
        relations_ref = self.db.collection("graph").document("relations").collection(user_id)
        
        for rel in relations:
            relation_id = str(uuid.uuid4())
            relations_ref.document(relation_id).set({
                "source": rel.get("source", "").lower(),
                "target": rel.get("target", "").lower(),
                "type": rel.get("type", "relates_to"),
                "user_id": user_id,
                "created_at": datetime.utcnow()
            })
            relation_ids.append(relation_id)
        
        return relation_ids
    
    async def get_entity_graph(self, user_id: str, entity_name: str) -> Dict[str, Any]:
        """
        Get graph data for a specific entity.
        
        Args:
            user_id: User ID
            entity_name: Name of entity to query
            
        Returns:
            Dict with nodes and edges
        """
        entity_name = entity_name.lower()
        
        # Get relations where entity is source or target
        relations_ref = self.db.collection("graph").document("relations").collection(user_id)
        
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
                "relation": data.get("type")
            })
        
        for doc in target_relations:
            data = doc.to_dict()
            nodes.add(data.get("source"))
            edges.append({
                "source": data.get("source"),
                "target": data.get("target"),
                "relation": data.get("type")
            })
        
        return {
            "nodes": [{"id": n, "label": n, "type": "entity"} for n in nodes],
            "edges": edges
        }
    
    async def save_document_metadata(self, user_id: str, filename: str, file_url: str, 
                                      file_type: str, chunks_count: int, summary: str = None) -> str:
        """
        Save document metadata to Firestore.
        
        Args:
            user_id: User ID
            filename: Original filename
            file_url: Firebase Storage URL
            file_type: Type (pdf, image, text)
            chunks_count: Number of chunks created
            summary: Optional document summary
            
        Returns:
            Document metadata ID
        """
        doc_id = str(uuid.uuid4())
        docs_ref = self.db.collection("documents").document(user_id).collection("files")
        
        data = {
            "filename": filename,
            "file_url": file_url,
            "type": file_type,
            "chunks_count": chunks_count,
            "user_id": user_id,
            "created_at": datetime.utcnow()
        }
        
        if summary:
            data["summary"] = summary
            
        docs_ref.document(doc_id).set(data)
        
        return doc_id


    async def get_user_documents(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all documents for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of document metadata
        """
        docs_ref = self.db.collection("documents").document(user_id).collection("files")
        docs = docs_ref.order_by("created_at", direction=firestore.Query.DESCENDING).get()
        
        results = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            # Convert datetime to ISO string
            if "created_at" in data and isinstance(data["created_at"], datetime):
                data["created_at"] = data["created_at"].isoformat()
            results.append(data)
            
        return results


firestore_service = FirestoreService()
