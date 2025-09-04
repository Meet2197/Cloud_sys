from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import files, folders, metadata, analytics

import os

ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(",")

app = FastAPI(title="Cloud Storage API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router)
app.include_router(folders.router)
app.include_router(metadata.router)
app.include_router(analytics.router)

@app.get("/")
async def root():
    return {"ok": True}
