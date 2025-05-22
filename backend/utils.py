import os
import json
import clip
import torch

def get_abs_path(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))

def is_image_file(filename):
    return filename.lower().endswith(('.jpg', '.jpeg', '.png'))

def load_metadata(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return {}

def load_clip_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess, device

