"""
Endee Client Wrapper - HTTP API Version
Handles all interactions with Endee vector database via HTTP
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class EndeeClient:
    """Client for interacting with Endee vector database via HTTP API"""
    
    def __init__(self):
        """Initialize Endee HTTP client"""
        self.base_url = os.getenv("ENDEE_HOST", "http://localhost:8080")
        self.api_key = os.getenv("ENDEE_API_KEY", None)
        
        # Prepare headers
        self.headers = {"Content-Type": "application/json"}
        if self.api_key:
            self.headers["Authorization"] = self.api_key
        
        print(f"  ✓ Endee HTTP client initialized ({self.base_url})")
    
    def create_index(
        self, 
        index_name: str = "support_tickets",
        dimension: int = 384,
        metric: str = "cosine"
    ) -> bool:
        """
        Create a vector index in Endee
        
        Args:
            index_name: Name of the index
            dimension: Vector dimension (384 for MiniLM)
            metric: Distance metric (cosine, euclidean, dot)
            
        Returns:
            bool: True if successful
        """
        try:
            # Convert metric to Endee's space_type
            space_type_map = {
                "cosine": "cosine",
                "euclidean": "l2",
                "dot": "ip"  # inner product
            }
            space_type = space_type_map.get(metric, "cosine")
            
            # Endee API format from source code
            payload = {
                "index_name": index_name,
                "dim": dimension,
                "space_type": space_type
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/index/create",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Created index '{index_name}' (dim: {dimension}, space_type: {space_type})")
                return True
            elif "already exists" in response.text.lower() or response.status_code == 409:
                print(f"ℹ️  Index '{index_name}' already exists")
                return True
            else:
                print(f"❌ Error creating index ({response.status_code}): {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Endee server. Is it running?")
            print("   Start it with: docker compose -f docker-compose-endee.yml up -d")
            return False
        except Exception as e:
            print(f"❌ Error creating index: {e}")
            return False
    
    def insert_vector(
        self,
        index_name: str,
        vector: List[float],
        metadata: Dict,
        vector_id: Optional[str] = None
    ) -> bool:
        """
        Insert a single vector into Endee
        
        Args:
            index_name: Name of the index
            vector: Embedding vector (384-dim for MiniLM)
            metadata: Associated metadata (category, priority, text, etc.)
            vector_id: Optional ID for the vector
            
        Returns:
            bool: True if successful
        """
        try:
            # Endee expects an array, so wrap single item
           return self.batch_insert(index_name, [vector], [metadata], [vector_id] if vector_id else None)
                
        except Exception as e:
            print(f"❌ Error inserting vector: {e}")
            return False
    
    def batch_insert(
        self,
        index_name: str,
        vectors: List[List[float]],
        metadatas: List[Dict],
        ids: Optional[List[str]] = None
    ) -> bool:
        """
        Insert multiple vectors at once (faster)
        
        Args:
            index_name: Name of the index
            vectors: List of embedding vectors
            metadatas: List of metadata dicts
            ids: Optional list of IDs
            
        Returns:
            bool: True if successful
        """
        try:
            # Build items array in Endee format
            # From source: expects array of {id, vector, sparse_indices, sparse_values}
            # We'll attach metadata as custom fields (Endee doesn't explicitly store metadata in vector insert)
            items = []
            for i, (vector, metadata) in enumerate(zip(vectors, metadatas)):
                item = {
                    "id": ids[i] if ids and i < len(ids) else str(i),
                    "vector": vector
                }
                # Note: Endee doesn't have built-in metadata storage in the vector insert API
                # Metadata would need to be stored separately or reconstructed from responses
                # For now, we'll just insert the vectors
                items.append(item)
            
            # Send as JSON array directly
            response = requests.post(
                f"{self.base_url}/api/v1/index/{index_name}/vector/insert",
                json=items,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Inserted {len(vectors)} vectors")
                return True
            else:
                print(f"❌ Error batch inserting ({response.status_code}): {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error batch inserting: {e}")
            return False
    
    def search(
        self,
        index_name: str,
        query_vector: List[float],
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar vectors in Endee
        
        Args:
            index_name: Name of the index to search
            query_vector: Query embedding vector
            top_k: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of results with scores and metadata
        """
        try:
            # Endee API format (from source code line 650: expects "k" and "vector")
            payload = {
                "vector": query_vector,
                "k": top_k,
                "include_vectors": False  # We don't need vectors back
            }
            
            if filters:
                payload["filter"] = filters  # TODO: Convert to Endee filter format if needed
            
            response = requests.post(
                f"{self.base_url}/api/v1/index/{index_name}/search",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                # Endee returns MessagePack, need to decode
                # For now, try JSON fallback or handle msgpack
                try:
                    # Try to decode as msgpack first
                    import msgpack
                    data = msgpack.unpackb(response.content, raw=False)
                except:
                    # Fallback to JSON
                    data = response.json()
                
                # Convert Endee format to our expected format
                # Endee returns: {results: [{id, distance, vector?, ...}]}
                results = []
                for item in data.get("results", []):
                    # Convert distance to similarity score (closer to 1 is more similar for cosine)
                    # For cosine: similarity = 1 - distance
                    distance = item.get("distance", 1.0)
                    score = 1.0 - distance if distance < 1.0 else 0.0
                    
                    results.append({
                        "score": score,
                        "metadata": {
                            "text": f"Similar ticket (id: {item.get('id', 'unknown')})",
                            "category": "Unknown",  # Endee doesn't store metadata with vectors
                            "priority": "Medium"
                        }
                    })
                return results
            else:
                print(f"❌ Error searching ({response.status_code}): {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error searching: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_stats(self, index_name: str = "support_tickets") -> Dict:
        """
        Get index statistics
        
        Args:
            index_name: Name of the index
            
        Returns:
            Dict with statistics
        """
        try:
            # Endee API: GET /api/v1/index/{index_name}/stats
            response = requests.get(
                f"{self.base_url}/api/v1/index/{index_name}/stats",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def delete_index(self, index_name: str) -> bool:
        """
        Delete an index (use with caution!)
        
        Args:
            index_name: Name of the index to delete
            
        Returns:
            bool: True if successful
        """
        try:
            # Endee API: DELETE /api/v1/index/{index_name}
            response = requests.delete(
                f"{self.base_url}/api/v1/index/{index_name}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Deleted index '{index_name}'")
                return True
            else:
                print(f"❌ Error deleting index: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting index: {e}")
            return False
