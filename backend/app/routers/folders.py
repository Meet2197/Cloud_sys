from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/folders", tags=["folders"])

@router.post("/", response_model=schemas.FolderOut)
async def create_folder(payload: schemas.FolderCreate, db: Session = Depends(get_db)):
    f = crud.create_folder(db, payload.name, payload.parent_id)
    return f

@router.get("/", response_model=list[schemas.FolderOut])
async def list_folders(db: Session = Depends(get_db)):
    return crud.list_folders(db)
