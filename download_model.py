"""
Download and cache the MiniLM model locally
This script downloads the all-MiniLM-L6-v2 model from Hugging Face
and saves it to the dataset directory
"""

from sentence_transformers import SentenceTransformer
import os

# Define model name and local save path
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
SAVE_PATH = './dataset/minilm_model'

def download_model():
    """Download and save the MiniLM model"""
    
    print("=" * 70)
    print("🚀 Downloading all-MiniLM-L6-v2 Model")
    print("=" * 70)
    print(f"\n📦 Model: {MODEL_NAME}")
    print(f"💾 Save Location: {SAVE_PATH}")
    print(f"📊 Model Details:")
    print(f"   - Output Dimensions: 384")
    print(f"   - Size: ~80 MB")
    print(f"   - Speed: Very Fast (CPU friendly)")
    print(f"   - Use Case: Semantic search, similarity matching")
    print("\n⏳ Starting download...\n")
    
    # Create directory if it doesn't exist
    os.makedirs(SAVE_PATH, exist_ok=True)
    
    # Download the model (this will take a minute on first run)
    model = SentenceTransformer(MODEL_NAME)
    
    # Save the model locally
    model.save(SAVE_PATH)
    
    print("\n✅ Model downloaded successfully!")
    print(f"📁 Saved to: {os.path.abspath(SAVE_PATH)}")
    
    # Test the model
    print("\n🧪 Testing model...")
    test_sentence = "I forgot my password"
    embedding = model.encode(test_sentence)
    
    print(f"   Test sentence: '{test_sentence}'")
    print(f"   Embedding shape: {embedding.shape}")
    print(f"   Embedding dimensions: {len(embedding)}")
    print(f"   First 5 values: {embedding[:5]}")
    
    print("\n" + "=" * 70)
    print("🎉 Setup Complete! You can now use the model in your project.")
    print("=" * 70)
    
    # Show how to load it later
    print("\n📝 How to use this model in your code:")
    print(f"""
from sentence_transformers import SentenceTransformer

# Load from local directory
model = SentenceTransformer('{SAVE_PATH}')

# Or load from Hugging Face (downloads if not cached)
model = SentenceTransformer('{MODEL_NAME}')

# Generate embeddings
text = "Your support ticket text"
embedding = model.encode(text)
print(embedding.shape)  # (384,)
    """)

if __name__ == "__main__":
    try:
        download_model()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have installed sentence-transformers:")
        print("   pip install sentence-transformers")
