"""
Index Sample Tickets into Endee
Loads sample tickets and stores their embeddings in Endee
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer
from src.endee_client import EndeeClient


def main():
    """Load sample tickets and index them in Endee"""
    
    print("\n" + "=" * 70)
    print("📚 Indexing Sample Tickets")
    print("=" * 70)
    
    # Load MiniLM model
    print("\n🤖 Loading MiniLM model...")
    model_path = "./dataset/minilm_model"
    
    if os.path.exists(model_path):
        model = SentenceTransformer(model_path)
        print(f"✅ Loaded model from: {model_path}")
    else:
        print(f"⚠️  Local model not found. Downloading from Hugging Face...")
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print(f"✅ Model loaded")
    
    # Load sample tickets
    print("\n📄 Loading sample tickets...")
    tickets_path = "./data/sample_tickets.json"
    
    if not os.path.exists(tickets_path):
        print(f"❌ {tickets_path} not found!")
        sys.exit(1)
    
    with open(tickets_path, 'r') as f:
        tickets = json.load(f)
    
    print(f"✅ Loaded {len(tickets)} tickets")
    
    # Initialize Endee client
    print("\n📡 Connecting to Endee...")
    client = EndeeClient()
    
    # Prepare batch data
    print("\n🔄 Generating embeddings...")
    vectors = []
    metadatas = []
    ids = []
    
    for ticket in tickets:
        # Generate embedding
        embedding = model.encode(ticket['text'], normalize_embeddings=True)
        
        # Prepare data
        vectors.append(embedding.tolist())
        metadatas.append({
            "category": ticket['category'],
            "priority": ticket['priority'],
            "text": ticket['text']
        })
        ids.append(f"ticket_{ticket['id']}")
        
        print(f"  ✓ Ticket {ticket['id']}: {ticket['text'][:50]}...")
    
    # Batch insert into Endee
    print(f"\n💾 Indexing {len(vectors)} tickets into Endee...")
    success = client.batch_insert(
        index_name="support_tickets",
        vectors=vectors,
        metadatas=metadatas,
        ids=ids
    )
    
    if success:
        print("\n" + "=" * 70)
        print("✅ Indexing Complete!")
        print("=" * 70)
        
        # Show statistics
        print("\n📊 Indexed Tickets by Category:")
        from collections import Counter
        category_counts = Counter(t['category'] for t in tickets)
        for category, count in category_counts.items():
            print(f"  • {category}: {count} tickets")
        
        print("\n🎯 Next steps:")
        print("1. Run: python main.py")
        print("2. Open: http://localhost:8000/docs")
        print("3. Test the /classify endpoint!")
    else:
        print("\n❌ Indexing failed. Check Endee connection.")
        sys.exit(1)


if __name__ == "__main__":
    main()
