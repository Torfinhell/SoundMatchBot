## **3. backend.md**

This file provides a comprehensive specification for the FastAPI backend, including file structure, classes, methods, and their purposes.

```markdown
# Backend Architecture

## Technology Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Vector Store**: FAISS (in‑memory, persisted to disk)
- **Cache**: Redis (for leaderboards and quick lookups)
- **Background Tasks**: Celery (optional, for embedding extraction)

## Folder Structure
backend/
├── main.py # FastAPI app entry point
├── config.py # Load settings from config.yaml
├── database.py # SQLAlchemy setup, engine, session
├── models.py # SQLAlchemy ORM models
├── schemas.py # Pydantic models for API requests/responses
├── redis_cache.py # Redis client and helper functions
├── faiss_index.py # FAISS index manager
├── music_extraction/ # Music feature extraction module
│ ├── clmr_extractor.py # Wrapper for CLMR model
│ └── youtube_dl.py # YouTube download utilities
├── routers/ # API route handlers
│ ├── users.py # User registration, profile
│ ├── polls.py # Poll creation, submission
│ ├── admin.py # Admin endpoints (protected)
│ └── recommendations.py # Ranking and matching
├── services/ # Business logic
│ ├── matching.py # User matching algorithm
│ ├── ranking.py # Ranking logic
│ └── embedding.py # Store/retrieve embeddings
└── utils/ # Helpers
├── security.py # Admin password check
└── validators.py # Input validation

text

## Database Models (`models.py`)

### `User`
- `id` (int, primary key)
- `telegram_id` (str, unique) – Telegram username or chat ID
- `telegram_username` (str, nullable)
- `created_at` (datetime)
- `is_admin` (bool, default False) – set via admin password flow
- `poll_answers` (relationship to `PollAnswer`)
- `embeddings` (relationship to `UserEmbedding`)

### `Poll`
- `id` (int, primary key)
- `title` (str)
- `questions` (JSON) – list of question strings
- `created_by_admin_id` (int, foreign key to User)
- `created_at` (datetime)
- `is_active` (bool)

### `PollAnswer`
- `id` (int, primary key)
- `user_id` (int, foreign key to User)
- `poll_id` (int, foreign key to Poll)
- `answers` (JSON) – mapping question index to answer text
- `submitted_at` (datetime)

### `UserEmbedding`
- `id` (int, primary key)
- `user_id` (int, foreign key to User)
- `cluster_id` (int) – which cluster (0..N_CLUSTERS-1)
- `embedding` (LargeBinary) – stored as bytes (float32 array)

### `MusicMetadata`
- `id` (int, primary key)
- `youtube_url` (str, unique)
- `title` (str)
- `author` (str)
- `extracted_at` (datetime)
- `embedding_ids` (JSON) – list of cluster embedding IDs (optional)

## API Endpoints (`routers/`)

### `users.py`
- `POST /register` – Register a new user (triggered by Telegram `/start`).  
  Request: `{ "telegram_id": str, "username": str }`  
  Response: `{ "user_id": int, "message": "ok" }`
- `GET /profile/{user_id}` – Get user profile info (poll answers, etc.)

### `polls.py`
- `POST /polls` – Create a new poll (admin only).  
  Request: `{ "title": str, "questions": list[str], "admin_password": str }`  
  Response: `{ "poll_id": int }`
- `POST /polls/{poll_id}/submit` – Submit poll answers.  
  Request: `{ "user_id": int, "answers": dict }`  
  Response: `{ "status": "submitted" }`
- `GET /polls/active` – List active polls for a user.

### `admin.py`
- `POST /admin/claim` – Claim admin rights.  
  Request: `{ "user_id": int, "password": str }`  
  Response: `{ "success": bool, "message": str }`
- `POST /admin/users/{user_id}/promote` – Promote a user to admin (super admin only). Requires special super admin password (optional).

### `recommendations.py`
- `GET /recommendations/{user_id}` – Get ranked list of recommended users.  
  Query params: `limit` (default 20)  
  Response: `[ { "user_id": int, "username": str, "score": float, "rank": int } ]`
- `GET /leaderboard` – Get global leaderboard (cached in Redis).  
  Response: same as above.

## Business Logic (`services/`)

### `matching.py`

**Class `Matcher`**
- `__init__(self, db_session, faiss_index, redis_client)`
- `def text_based_filter(self, user_id: int, top_k: int) -> list[int]`  
  Retrieves users whose poll answers, song authors, or titles match the given user's profile. Uses TF‑IDF or simple keyword matching. Returns candidate user IDs.
- `def music_based_rerank(self, user_id: int, candidates: list[int]) -> list[tuple[int, float]]`  
  For each candidate, compute similarity between user's music embeddings (centroid of clusters) and candidate's embeddings. Returns sorted list of (user_id, similarity).
- `def get_recommendations(self, user_id: int, limit: int) -> list[dict]`  
  Orchestrates: text filter → music rerank → format output.

### `ranking.py`

**Class `RankingService`**
- `def update_leaderboard(self)` – Recomputes global rankings (e.g., every hour) and stores in Redis.
- `def get_leaderboard(self, limit: int) -> list[dict]` – Fetches from Redis or recomputes if stale.
- `def compute_scores(self, user_ids: list[int]) -> dict[int, float]` – Uses matching algorithm to compute pairwise scores (optional).

### `embedding.py`

**Class `EmbeddingService`**
- `def store_embedding(self, user_id: int, cluster_id: int, embedding: list[float])` – Saves to FAISS and PostgreSQL.
- `def get_user_embeddings(self, user_id: int) -> list[np.ndarray]` – Retrieves all cluster embeddings for a user.
- `def get_centroid(self, user_id: int) -> np.ndarray` – Computes average of user's embeddings.
- `def similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float` – Cosine similarity.

## FAISS Index Management (`faiss_index.py`)

**Class `FAISSWrapper`**
- `__init__(self, dimension: int = 512)` – CLMR embeddings dimension (adjust based on model).
- `def add(self, user_id: int, cluster_id: int, embedding: np.ndarray)` – Adds vector to index; stores mapping from vector ID to (user_id, cluster_id).
- `def search(self, query: np.ndarray, k: int) -> list[tuple[int, float]]` – Returns top‑k user_ids and scores (aggregate per user).
- `def save(self, path: str)` / `def load(self, path: str)` – Persist index.

## Redis Cache (`redis_cache.py`)

**Functions**
- `cache_leaderboard(leaderboard: list)` – Store JSON in Redis with TTL.
- `get_cached_leaderboard() -> list` – Retrieve if exists.
- `invalidate_leaderboard()` – Clear cache after updates.

## Configuration (`config.py`)

Loads settings from `config.yaml` (see `readme_creation.md`). Provides attributes:
- `DATABASE_URL`
- `REDIS_HOST`, `REDIS_PORT`
- `N_CLUSTERS` (int)
- `NUM_PEOPLE_REFILTER` (int)
- `ADMIN_PASSWORD` (str)
- `FAISS_INDEX_PATH` (str)
- `EMBEDDING_DIM` (int)
- `CORS_ORIGINS` (list)

## Main Application (`main.py`)

- Creates FastAPI app.
- Includes routers.
- Sets up CORS.
- Initializes database, FAISS, Redis.
- Lifespan events to load/save FAISS index.
- Health check endpoint.
