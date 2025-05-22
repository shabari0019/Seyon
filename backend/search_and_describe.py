# backend/search_and_describe.py

import clip
import torch
from PIL import Image
import numpy as np
import faiss
import json
import os

# Paths


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "gallery.index")
FEATURES_PATH = os.path.join(BASE_DIR, "gallery_features.npy")
FILENAMES_PATH = os.path.join(BASE_DIR, "gallery_filenames.npy")
METADATA_PATH = os.path.join(BASE_DIR, "../metadata.json")
GALLERY_DIR = os.path.join(BASE_DIR,"../gallery/")

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load CLIP model
model, preprocess = clip.load("ViT-B/32", device=device)

# Load FAISS index and filenames
index = faiss.read_index(INDEX_PATH)
filenames = np.load(FILENAMES_PATH)

# Load metadata
with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

def extract_feature(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        feature = model.encode_image(image)
        feature = feature / feature.norm(dim=-1, keepdim=True)
    return feature.cpu().numpy().astype("float32")

def search_and_describe(query_image_path, top_k=3):
    query_vector = extract_feature(query_image_path)
    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        filename = filenames[idx]
        info = metadata.get(filename, {})
        results.append({
            "filename": filename,
            "title": info.get("title", "Unknown"),
            "description": info.get("description", "No description found.")
        })

    return results
