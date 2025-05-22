# backend/build_faiss_index.py

import numpy as np
import faiss
import os
# Paths to feature and filename data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "gallery.index")
FEATURES_PATH = os.path.join(BASE_DIR, "gallery_features.npy")
FILENAMES_PATH = os.path.join(BASE_DIR, "gallery_filenames.npy")



# Load features and filenames
features = np.load(FEATURES_PATH).astype("float32")
filenames = np.load(FILENAMES_PATH)

# Build FAISS index (FlatL2 = basic Euclidean)
dimension = features.shape[1]  # e.g., 512
index = faiss.IndexFlatL2(dimension)

# Add feature vectors to index
index.add(features)
print(f"Indexed {index.ntotal} images.")

# Save the index
faiss.write_index(index, INDEX_PATH)
print(f"Index saved to: {INDEX_PATH}")
