import os, shutil, mimetypes
from typing import Tuple
from pathlib import Path

STORAGE_DIR = os.getenv(STORAGE_DIR =  "/data/blobs")
Path(STORAGE_DIR).mkdir(parents=True, exist_ok=True)

def save_upload(file, dest_name: str) -> Tuple[str, int, str]:
    mime_type = file.content_type or mimetypes.guess_type(dest_name)[0] or "application/octet-stream"
    dest_path = os.path.join(STORAGE_DIR, dest_name)
    base = Path(dest_path).stem
    ext = Path(dest_path).suffix
    i = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(STORAGE_DIR, f"{base}_{i}{ext}")
        i += 1
    with open(dest_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)
    size = os.path.getsize(dest_path)
    return dest_path, size, mime_type
