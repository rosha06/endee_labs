"""
Setup Endee Index
One-time script to create the vector index in Endee
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.endee_client import EndeeClient


def main():
    """Create support tickets index in Endee"""
    
    print("\n" + "=" * 70)
    print("🚀 Endee Index Setup")
    print("=" * 70)
    
    # Initialize client
    print("\n📡 Connecting to Endee...")
    client = EndeeClient()
    
    # Create index
    print("\n📊 Creating 'support_tickets' index...")
    success = client.create_index(
        index_name="support_tickets",
        dimension=384,  # MiniLM output dimension
        metric="cosine"  # Cosine similarity for text embeddings
    )
    
    if success:
        print("\n" + "=" * 70)
        print("✅ Setup Complete!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Run: python scripts/index_tickets.py")
        print("2. Run: python main.py")
        print("3. Test: http://localhost:8000/docs")
    else:
        print("\n❌ Setup failed. Check Endee connection.")
        print("\nTroubleshooting:")
        print("1. Is Endee server running?")
        print("2. Check ENDEE_HOST in .env file")
        print("3. Try: docker run -p 6333:6333 endee/endee")
        sys.exit(1)


if __name__ == "__main__":
    main()
