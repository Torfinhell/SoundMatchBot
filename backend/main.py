from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import users, polls, admin, recommendations
from .faiss_index import faiss_index
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    faiss_index.load(settings.backend.faiss_index_path)
    yield
    faiss_index.save(settings.backend.faiss_index_path)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(polls.router)
app.include_router(admin.router)
app.include_router(recommendations.router)