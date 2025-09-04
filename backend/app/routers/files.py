from fastapi import APIRouter, Depends, UploadFile, File as UpFile, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db, Base, engine
from .. import crud, models, storage, schemas
import os
from typing import Optional

router = APIRouter(prefix="/files", tags=["files"])

Base.metadata.create_all(bind=engine)

@router.post("/upload", response_model=schemas.FileOut)
async def upload_file(
    f: UploadFile = UpFile(...),
    folder_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    dest, size, mime = storage.save_upload(f, f.filename)
    name = os.path.basename(dest)
    kind = "image" if mime.startswith("image/") else "text" if mime.startswith("text/") else "video" if mime.startswith("video/") else "other"
    file = crud.create_file(db, name=name, mime=mime, size=size, path=dest, kind=kind, folder_id=folder_id)
    meta_json = {"nd_pyramid": []}
    crud.upsert_metadata(db, file.id, json=meta_json, tags="")
    return file

@router.get("/", response_model=list[schemas.FileOut])
async def list_files(q: Optional[str] = None, kind: Optional[str] = None, cluster_id: Optional[int] = None, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    rows, _ = crud.search_files(db, q, kind, cluster_id, limit, offset)
    return rows

@router.get("/{file_id}", response_model=schemas.FileDetail)
async def file_detail(file_id: int, db: Session = Depends(get_db)):
    f = crud.get_file(db, file_id)
    if not f:
        raise HTTPException(404, "File not found")
    return schemas.FileDetail(**f.__dict__, metadata=(f.metadata.json if f.metadata else None))

@router.get("/{file_id}/download")
async def download(file_id: int, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse
    f = crud.get_file(db, file_id)
    if not f:
        raise HTTPException(404, "File not found")
    return FileResponse(f.path, media_type=f.mime_type, filename=f.name)

@router.delete("/{file_id}")
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    f = crud.get_file(db, file_id)
    if not f:
        raise HTTPException(404, "File not found")
    f.deleted = True
    db.commit()
    return {"ok": True}
