# backend/extract_features.py

import os
import numpy as np
from PIL import Image
import clip
import torch

GALLERY_DIR = "../gallery/"
FEATURES_SAVE_PATH = "../backend/gallery_features.npy"
FILENAMES_SAVE_PATH = "../backend/gallery_filenames.npy"

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load CLIP model
model, preprocess = clip.load("ViT-B/32", device=device)

# Containers
features = []
filenames = []

# Loop over images
for filename in os.listdir(GALLERY_DIR):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(GALLERY_DIR, filename)
        image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

        with torch.no_grad():
            feature = model.encode_image(image)
            feature = feature / feature.norm(dim=-1, keepdim=True)  # Normalize
            features.append(feature.cpu().numpy())
            filenames.append(filename)

# Stack features
features = np.vstack(features)

# Save features and filenames
np.save(FEATURES_SAVE_PATH, features)
np.save(FILENAMES_SAVE_PATH, np.array(filenames))

print(f"Saved {len(filenames)} feature vectors to {FEATURES_SAVE_PATH}")
