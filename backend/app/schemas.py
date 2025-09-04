from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, List

class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

class FolderOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    model_config = ConfigDict(from_attributes=True)

class FileOut(BaseModel):
    id: int
    name: str
    mime_type: str
    size: int
    kind: str
    folder_id: Optional[int]
    created_at: Any
    model_config = ConfigDict(from_attributes=True)

class FileDetail(FileOut):
    metadata: Optional[dict] = None

class MetadataUpdate(BaseModel):
    json: dict
    tags: str

class ClusterNode(BaseModel):
    id: int
    label: str
    cluster: int

class ClusterGraph(BaseModel):
    nodes: List[ClusterNode]
    edges: List[tuple]
