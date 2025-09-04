from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Folder(Base):
    __tablename__ = "folders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    children = relationship("Folder")
    files = relationship("File", back_populates="folder")

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    path = Column(String, unique=True, index=True)
    mime = Column(String)
    size = Column(Integer)
    kind = Column(String)
    folder_id = Column(Integer, ForeignKey("folders.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)

    folder = relationship("Folder", back_populates="files")
    file_metadata = relationship("Metadata", back_populates="file")

class Metadata(Base):
    __tablename__ = "metadata"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    json = Column(JSON)
    tags = Column(String)

    file = relationship("File", back_populates="file_metadata")

class ClusterAssignment(Base):
    __tablename__ = "cluster_assignments"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("files.id"), index=True)
    cluster_id = Column(Integer, index=True)
    score = Column(Integer, default=0)
