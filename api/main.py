"""FastAPI application for the concert discovery API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.concerts import router as concerts_router

app = FastAPI(
    title="Kids Concert Finder",
    description="API for discovering child-friendly concerts in Boston metro area",
    version="0.1.0",
)

# CORS for local React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(concerts_router)
