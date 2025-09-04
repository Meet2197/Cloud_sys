from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models, schemas

router = APIRouter(prefix="/metadata", tags=["metadata"])

@router.patch("/{file_id}", response_model=schemas.FileDetail)
async def update_metadata(file_id: int, payload: schemas.MetadataUpdate, db: Session = Depends(get_db)):
    f = crud.get_file(db, file_id)
    if not f:
        raise HTTPException(404, "File not found")
    md = crud.upsert_metadata(db, file_id, payload.json, payload.tags)
    return schemas.FileDetail(**f.__dict__, metadata=md.json)
