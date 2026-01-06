"""
Generate Text Embeddings for Complaint Texts
Uses sentence-transformers to create semantic embeddings
Embeddings will be stored in MongoDB for semantic search
"""

import pandas as pd
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings('ignore')


def generate_complaint_embeddings():
    """Generate embeddings for all complaint texts"""
    
    print("=" * 60)
    print("COMPLAINT TEXT EMBEDDINGS GENERATION")
    print("=" * 60)
    
    # Load dataset
    print("\n[1/4] Loading dataset...")
    df = pd.read_csv('../apartment_management_dataset_300.csv')
    print(f"   ✓ Loaded {len(df)} records")
    
    # Load pre-trained sentence transformer model
    print("\n[2/4] Loading sentence transformer model...")
    print("   (This may take a moment on first run)")
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight, fast model
    print("   ✓ Model loaded: all-MiniLM-L6-v2 (384 dimensions)")
    
    # Generate embeddings
    print("\n[3/4] Generating embeddings for complaint texts...")
    complaint_texts = df['complaint_text'].tolist()
    embeddings = model.encode(
        complaint_texts,
        show_progress_bar=True,
        batch_size=32
    )
    print(f"   ✓ Generated {len(embeddings)} embeddings")
    print(f"   ✓ Embedding shape: {embeddings.shape}")
    
    # Create embeddings dataframe
    embeddings_df = pd.DataFrame({
        'complaint_id': df['complaint_id'],
        'complaint_text': df['complaint_text'],
        'embedding': embeddings.tolist()
    })
    
    # Save embeddings
    print("\n[4/4] Saving embeddings...")
    
    # Save as pickle for Python use
    with open('complaint_embeddings.pkl', 'wb') as f:
        pickle.dump(embeddings_df, f)
    print("   ✓ Saved: complaint_embeddings.pkl")
    
    # Save as CSV for MongoDB import
    embeddings_df['embedding_str'] = embeddings_df['embedding'].apply(lambda x: ','.join(map(str, x)))
    embeddings_df[['complaint_id', 'complaint_text', 'embedding_str']].to_csv(
        'complaint_embeddings.csv',
        index=False
    )
    print("   ✓ Saved: complaint_embeddings.csv")
    
    # Test similarity search
    print("\n[TESTING] Sample similarity search:")
    test_query = "Electric socket sparking"
    query_embedding = model.encode([test_query])[0]
    
    # Calculate cosine similarity
    from sklearn.metrics.pairwise import cosine_similarity
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    
    # Get top 3 most similar complaints
    top_indices = similarities.argsort()[-3:][::-1]
    
    print(f"\n   Query: '{test_query}'")
    print("   Top 3 most similar complaints:")
    for i, idx in enumerate(top_indices, 1):
        print(f"   {i}. '{df.iloc[idx]['complaint_text']}' "
              f"(similarity: {similarities[idx]:.3f})")
    
    print("\n" + "=" * 60)
    print("✅ EMBEDDINGS GENERATION COMPLETE!")
    print("=" * 60)
    print("\nℹ️  These embeddings can be used for:")
    print("   • Semantic search of similar complaints")
    print("   • Complaint clustering and categorization")
    print("   • Automated complaint routing")
    print("   • Duplicate complaint detection")
    
    return embeddings_df, model


if __name__ == "__main__":
    generate_complaint_embeddings()
