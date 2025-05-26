import os
import numpy as np
import faiss
import torch
from PIL import Image
from utils import get_abs_path, is_image_file, load_clip_model

GALLERY_DIR = get_abs_path("../gallery")
FEATURES_PATH = get_abs_path("gallery_features.npy")
FILENAMES_PATH = get_abs_path("gallery_filenames.npy")
INDEX_PATH = get_abs_path("gallery.index")

model, preprocess, device = load_clip_model()

def extract_features():
    features, filenames = [], []
    for file in os.listdir(GALLERY_DIR):
        if is_image_file(file):
            path = os.path.join(GALLERY_DIR, file)
            try:
                image = preprocess(Image.open(path)).unsqueeze(0).to(device)
                with torch.no_grad():
                    feature = model.encode_image(image)
                    feature = feature / feature.norm(dim=-1, keepdim=True)
                    features.append(feature.cpu().numpy())
                    filenames.append(file)
            except:
                print(f"⚠️ Skipped: {file}")
    features = np.vstack(features)
    np.save(FEATURES_PATH, features)
    np.save(FILENAMES_PATH, filenames)
    return

def build_index(features):
    dim = features.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(features.astype("float32"))
    faiss.write_index(index, INDEX_PATH)

if __name__ == "__main__":
    print("🔄 Extracting features and building index...")
    features = extract_features()
    build_index(features)
    print("✅ Setup complete!")