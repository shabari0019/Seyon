import zipfile
import os

# Zip file path
zip_path = "mock_tourist_dataset.zip"

# Create zip containing gallery and metadata
with zipfile.ZipFile(zip_path, 'w') as zipf:
    # Add metadata.json
    zipf.write("/data/metadata.json", arcname="metadata.json")
    # Add gallery images
    for file in os.listdir("/data/mock_gallery"):
        zipf.write(os.path.join("/data/mock_gallery", file), arcname=f"mock_gallery/{file}")


