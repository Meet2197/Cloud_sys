"""Seed script: creates example folders, sample files, metadata and sample blobs."""
import os, shutil, json
from app.database import SessionLocal, Base, engine
from app import models, crud
from pathlib import Path

def ensure_db():
    Base.metadata.create_all(bind=engine)

def create_blob(filename: str, content: bytes):
    blobs_dir = os.getenv('STORAGE_DIR', os.path.join(os.getcwd(), 'data', 'blobs'))
    Path(blobs_dir).mkdir(parents=True, exist_ok=True)
    p = Path(blobs_dir) / filename
    p.write_bytes(content)
    return str(p), p.stat().st_size, 'text/plain'

def run_seed():
    ensure_db()
    db = SessionLocal()
    try:
        # create folders
        root = crud.create_folder(db, 'My Drive', None)
        pics = crud.create_folder(db, 'Pictures', root.id)
        docs = crud.create_folder(db, 'Documents', root.id)

        # create sample blobs
        p1, s1, m1 = create_blob('hello.txt', b'Hello world sample file')
        f1 = crud.create_file(db, name='hello.txt', mime=m1, size=s1, path=p1, kind='text', folder_id=docs.id)
        crud.upsert_metadata(db, f1.id, {'description':'Sample text file', 'nd_pyramid': []}, 'sample text')

        p2, s2, m2 = create_blob('image_sample.jpg', b'\xff\xd8\xff\xdb\x00' + b'JPEGPLACEHOLDER')
        f2 = crud.create_file(db, name='image_sample.jpg', mime='image/jpeg', size=s2, path=p2, kind='image', folder_id=pics.id)
        crud.upsert_metadata(db, f2.id, {'description':'Sample image', 'nd_pyramid': ['low','mid','high']}, 'image sample')

        print('Seed complete.')
    finally:
        db.close()

if __name__ == '__main__':
    run_seed()
