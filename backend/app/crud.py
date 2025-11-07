from sqlalchemy.orm import Session
from . import models
from typing import Optional, List, Dict, Any

def create_folder(db: Session, name: str, parent_id: Optional[int]):
    f = models.Folder(name=name, parent_id=parent_id)
    db.add(f)
    db.commit()
    db.refresh(f)
    return f

def list_folders(db: Session):
    return db.query(models.Folder).all()

def create_file(db: Session, *, name: str, mime: str, size: int, path: str, kind: str, folder_id: Optional[int]):
    f = models.File(name=name, mime=mime, size=size, path=path, kind=kind, folder_id=folder_id)
    db.add(f)
    db.commit()
    db.refresh(f)
    return f

def upsert_metadata(db: Session, file_id: int, json: Dict[str, Any], tags: str):
    md = db.query(models.FileMetadata).filter(models.FileMetadata.file_id == file_id).first()
    if md:
        md.json = json
        md.tags = tags
    else:
        md = models.FileMetadata(file_id=file_id, json=json, tags=tags)
        db.add(md)
    db.commit()
    db.refresh(md)
    return md

def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.id == file_id, models.File.deleted == False).first()

def search_files(db: Session, query: Optional[str], kind: Optional[str], cluster_id: Optional[int], limit=50, offset=0):
    q = db.query(models.File).filter(models.File.deleted == False)
    if query:
        like = f"%{query}%"
        q = q.filter(models.File.name.like(like))
    if kind:
        q = q.filter(models.File.kind == kind)
    if cluster_id is not None:
        from sqlalchemy import select
        from sqlalchemy.orm import aliased
        ca = aliased(models.ClusterAssignment)
        q = q.join(ca, ca.file_id == models.File.id).filter(ca.cluster_id == cluster_id)
    total = q.count()
    rows = q.order_by(models.File.created_at.desc()).offset(offset).limit(limit).all()
    return rows, total

def set_cluster_assignments(db: Session, mapping: dict):
    from sqlalchemy import delete
    db.execute(delete(models.ClusterAssignment))
    for fid, cid in mapping.items():
        db.add(models.ClusterAssignment(file_id=fid, cluster_id=cid))
    db.commit()
