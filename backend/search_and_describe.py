import numpy as np
import faiss
import torch
from PIL import Image
from utils import get_abs_path, load_clip_model, load_metadata, is_image_file

model, preprocess, device = load_clip_model()

INDEX_PATH = get_abs_path("gallery.index")
FEATURES_PATH = get_abs_path("gallery_features.npy")
FILENAMES_PATH = get_abs_path("gallery_filenames.npy")
METADATA_PATH = get_abs_path("../metadata.json")

index = faiss.read_index(INDEX_PATH)
features = np.load(FEATURES_PATH)
filenames = np.load(FILENAMES_PATH)
metadata = load_metadata(METADATA_PATH)

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
        fname = filenames[idx]
        info = metadata.get(fname, {})
        results.append({
            "filename": fname,
            "title": info.get("title", "Unknown"),
            "description": info.get("description", "No description found.")
        })
    return results

