# Final Project Prompt

Use the following markdown files to create a complete, runnable project. Ensure all components are compatible and follow the specifications exactly.

## Project Overview
A Telegram bot + web dashboard that matches users based on music taste. Users register via Telegram, answer polls, and get ranked recommendations of other users with similar music preferences. Admin can create groups and polls. Matching uses text (poll answers, song authors, titles) and music embeddings (extracted from YouTube audio via CLMR). Fast updates with Redis caching.

## Required Components
- **Backend (FastAPI)** – handles API, database, embeddings, matching logic.
- **Frontend (Telegram Bot + React/Vite)** – user interaction and admin dashboard.
- **Music Extraction** – CLMR model for audio embeddings from YouTube.
- **Database** – PostgreSQL for metadata, FAISS for embeddings, Redis for caching.
- **Configuration** – single config file with backend/frontend sections.
- **LLM Council** – optional installation guide; not integrated in code.

## Provided Prompts
- `llm_council_installation.md` – how to install and run LLM Council.
- `backend.md` – detailed backend architecture, classes, methods.
- `frontend.md` – detailed frontend architecture, Telegram bot handlers, React components.
- `music_extraction.md` – steps to extract embeddings using CLMR.
- `readme_creation.md` – content for README.md, including config explanation.
- `Create_Presenation.md` – outline for project presentation.
- `testing_and_metrics.md` – testing plan and metrics.
- `AI_example.md` – example file for LLM Council demo.

## Development Steps
1. Set up PostgreSQL and Redis.
2. Create config file (config.yaml) as per `readme_creation.md`.
3. Implement backend following `backend.md`.
4. Implement music extraction script and integrate with backend.
5. Implement Telegram bot and React dashboard following `frontend.md`.
6. Write tests as described in `testing_and_metrics.md`.
7. (Optional) Set up LLM Council per `llm_council_installation.md` for demos.

All prompts must be followed precisely to ensure compatibility.





Configuration (config.ts)
Reads from environment variables (Vite's import.meta.env) or a shared config served by backend. Exports:

BACKEND_URL

ADMIN_PASSWORD (only used for UI hint)

DEFAULT_LIMIT (ranking count)

Running the Dashboard
bash
cd frontend/web
npm install
npm run dev
Interaction with Backend
Both bot and web dashboard use the same REST API endpoints defined in backend.md. They must handle authentication via telegram_id passed in headers or body.

text

---

## **5. music_extraction.md**

This file provides step‑by‑step instructions for extracting music embeddings using CLMR, including notebooks and integration with the backend.

```markdown
# Music Feature Extraction with CLMR

This guide explains how to extract audio embeddings from YouTube music using the [CLMR](https://github.com/spijkervet/CLMR) model.

## Prerequisites
- Python 3.8+
- `ffmpeg` installed on system
- CUDA (optional, for GPU)

## Installation

Clone the CLMR repository and install dependencies:
```bash
git clone https://github.com/spijkervet/CLMR.git
cd CLMR
pip install -r requirements.txt
Notebooks
Two Jupyter notebooks are provided in the sample_notebooks/ folder:

1. youtube_music_extraction.ipynb
Downloads audio from a YouTube playlist or single video.

Steps:

Use pytube or yt-dlp to download audio as MP3/WAV.

Convert to 16kHz mono (required by CLMR).

Save audio files to a local directory.

Output: Folder with audio files.

2. music_extraction.ipynb
Extracts embeddings using the pretrained CLMR model.

Steps:

Load the CLMR model (e.g., clmr==0.0.5 or custom checkpoint).

For each audio file, compute embeddings for fixed‑length segments.

Aggregate embeddings (mean, max, or cluster) to produce a fixed‑size representation per track.

Save embeddings as NumPy arrays, along with metadata (YouTube URL, title, author).

Cluster Generation:

Use N_CLUSTERS from config.

Apply k‑means on all segment embeddings of a track to get cluster centroids.

Store each centroid as a separate embedding vector.

Integration with Backend
The backend should have a service that:

Accepts a YouTube URL (from admin input).

Downloads audio (using yt-dlp).

Extracts embeddings via a Python wrapper that calls the CLMR model.

Stores embeddings in FAISS and metadata in PostgreSQL.

Wrapper class example (clmr_extractor.py):

python
import torch
import numpy as np
from clmr.models import SampleCNN

class CLMRExtractor:
    def __init__(self, model_path=None, device='cuda'):
        self.device = device
        self.model = SampleCNN( ... )  # load pretrained
        self.model.eval()
    
    def extract_embeddings(self, audio_path: str) -> np.ndarray:
        # Load audio, preprocess, run model
        # Return embeddings (n_segments x dim)
        pass

    def extract_clusters(self, audio_path: str, n_clusters: int) -> np.ndarray:
        # Extract embeddings, then k-means
        # Return n_clusters x dim centroids
        pass
Background Task:
Since extraction can be slow, use Celery or FastAPI's BackgroundTasks to process URLs asynchronously.

Database Storage:

After extraction, store each cluster embedding in UserEmbedding (if linked to a user) or in a separate MusicEmbedding table for songs.

Update the user's profile with references to these embeddings for matching.

Note: Ensure the FAISS index is updated when new embeddings are added.

text

---

## **6. readme_creation.md**

This file will contain the content for the project's main README.md, including installation, configuration, and usage.

```markdown
# SoundMatchBot

A Telegram bot and web dashboard that matches users based on music taste using audio embeddings and poll data.

## Features
- Telegram bot for user interaction (dark theme UI).
- Web dashboard for admin and rankings.
- Polls to collect music preferences.
- Music embedding extraction from YouTube using CLMR.
- User matching via text (poll answers, song metadata) and audio embeddings.
- Redis‑cached leaderboard for fast updates.
- Configurable via single YAML file.

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 13+
- Redis 6+
- `ffmpeg` (for audio processing)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SoundMatchBot.git
   cd SoundMatchBot
Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
Install Python dependencies:

bash
pip install -r backend/requirements.txt
Set up PostgreSQL and Redis (refer to their official guides).

Copy config.example.yaml to config.yaml and edit with your settings (see Configuration section).

Initialize the database:

bash
cd backend
python -m scripts.init_db
Run the FastAPI server:

bash
uvicorn main:app --reload