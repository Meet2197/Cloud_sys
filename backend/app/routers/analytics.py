from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, crud
from ..knn import compute_clusters
from ..schemas import ClusterGraph, ClusterNode

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.post("/recluster", response_model=ClusterGraph)
async def recluster(db: Session = Depends(get_db)):
    q = db.query(models.File, models.FileMetadata).join(models.FileMetadata, models.File.id == models.FileMetadata.file_id, isouter=True).filter(models.File.deleted == False).all()
    items = []
    for f, md in q:
        items.append({
            "id": f.id,
            "name": f.name,
            "tags": (md.tags if md else ""),
            "meta_json": (md.json if md else {}),
        })
    result = compute_clusters(items)
    crud.set_cluster_assignments(db, result["assignments"])

    nodes = [ClusterNode(id=it["id"], label=it["name"], cluster=result["assignments"][it["id"]]) for it in items]
    edges = result["edges"]
    return ClusterGraph(nodes=nodes, edges=edges)

@router.get("/clusters", response_model=ClusterGraph)
async def get_clusters(db: Session = Depends(get_db)):
    q = db.query(models.File, models.ClusterAssignment).join(models.ClusterAssignment, models.ClusterAssignment.file_id == models.File.id, isouter=True).filter(models.File.deleted == False).all()
    nodes = []
    for f, ca in q:
        cid = ca.cluster_id if ca else -1
        nodes.append({"id": f.id, "label": f.name, "cluster": cid})
    return ClusterGraph(nodes=nodes, edges=[])
