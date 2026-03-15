from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

try:
    from .config import settings
    from .routers import users, polls, admin, recommendations
    from .faiss_index import faiss_index
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root with: uvicorn backend.main:app --reload")
    raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Load FAISS index on startup
        index_path = settings.backend.faiss_index_path
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss_index.load(index_path)
        print(f"Loaded FAISS index from {index_path}")
    except Exception as e:
        print(f"Warning: Could not load FAISS index: {e}")
        print("This is normal for first run - index will be created when needed.")

    yield

    try:
        # Save FAISS index on shutdown
        faiss_index.save(settings.backend.faiss_index_path)
        print(f"Saved FAISS index to {settings.backend.faiss_index_path}")
    except Exception as e:
        print(f"Warning: Could not save FAISS index: {e}")

app = FastAPI(
    title="SoundMatchBot API",
    description="Music-based social matching platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
try:
    app.include_router(users.router)
    app.include_router(polls.router)
    app.include_router(admin.router)
    app.include_router(recommendations.router)
    print("All routers loaded successfully")
except Exception as e:
    print(f"Error loading routers: {e}")
    raise

@app.get("/")
async def root():
    return {"message": "SoundMatchBot API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}