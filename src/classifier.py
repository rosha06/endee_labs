"""
Ticket Classifier
Uses MiniLM embeddings and Endee vector search to classify support tickets
"""

import os
from typing import Dict, List
from collections import Counter
from sentence_transformers import SentenceTransformer
from src.endee_client import EndeeClient


class TicketClassifier:
    """Classify support tickets using semantic search"""
    
    def __init__(self, model_path: str = "./dataset/minilm_model"):
        """
        Initialize classifier
        
        Args:
            model_path: Path to MiniLM model
        """
        print("🤖 Initializing Ticket Classifier...")
        
        # Load MiniLM model
        if os.path.exists(model_path):
            self.model = SentenceTransformer(model_path)
            print(f"  ✓ Loaded model from {model_path}")
        else:
            print(f"  ⚠️  Loading from Hugging Face...")
            self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print(f"  ✓ Model loaded")
        
        # Initialize Endee client
        self.endee = EndeeClient()
        print("  ✓ Endee client initialized")
        
        # Routing configuration
        self.routing_map = {
            "Authentication": "Security Team",
            "Billing": "Billing Team",
            "Technical": "Technical Support",
            "Feature Request": "Product Team",
            "General Inquiry": "Customer Support"
        }
    
    def classify(self, ticket_text: str, top_k: int = 5) -> Dict:
        """
        Classify a support ticket
        
        Args:
            ticket_text: The ticket description
            top_k: Number of similar tickets to retrieve
            
        Returns:
            Classification result with category, priority, confidence
        """
        # Generate embedding
        embedding = self.model.encode(ticket_text, normalize_embeddings=True)
        
        # Search Endee for similar tickets
        results = self.endee.search(
            index_name="support_tickets",
            query_vector=embedding.tolist(),
            top_k=top_k
        )
        
        if not results:
            return {
                "category": "Unclassified",
                "priority": "Medium",
                "confidence": 0.0,
                "routing_team": "General Support",
                "similar_tickets": []
            }
        
        # Extract categories and priorities
        categories = [r['metadata']['category'] for r in results]
        priorities = [r['metadata']['priority'] for r in results]
        
        # Vote for most common category/priority
        category_counts = Counter(categories)
        priority_counts = Counter(priorities)
        
        predicted_category = category_counts.most_common(1)[0][0]
        predicted_priority = priority_counts.most_common(1)[0][0]
        
        # Calculate confidence (average similarity)
        avg_similarity = sum(r['score'] for r in results) / len(results)
        
        # Get routing team
        routing_team = self.routing_map.get(predicted_category, "General Support")
        
        # Prepare similar tickets info
        similar_tickets = [
            {
                "text": r['metadata']['text'],
                "category": r['metadata']['category'],
                "priority": r['metadata']['priority'],
                "similarity": round(r['score'], 3)
            }
            for r in results[:3]  # Top 3 most similar
        ]
        
        return {
            "category": predicted_category,
            "priority": predicted_priority,
            "confidence": round(avg_similarity, 3),
            "routing_team": routing_team,
            "similar_tickets": similar_tickets
        }
    
    def get_categories(self) -> List[str]:
        """Get list of available categories"""
        return list(self.routing_map.keys())
