Telegram Bot Setup
Create a bot via @BotFather and get the token.

Add the token to config.yaml under bot.token.

Run the bot:

bash
cd frontend/telegram_bot
python main.py
Web Dashboard Setup
Navigate to the web frontend:

bash
cd frontend/web
npm install
Copy .env.example to .env and set VITE_BACKEND_URL (e.g., http://localhost:8000).

Start the dev server:

bash
npm run dev
Open http://localhost:5173 in your browser.

Configuration
The config.yaml file contains all settings. Example:

yaml
backend:
  database_url: postgresql://user:pass@localhost/soundmatch
  redis_host: localhost
  redis_port: 6379
  n_clusters: 10
  num_people_refilter: 50
  admin_password: "your_secure_password"
  faiss_index_path: ./data/faiss.index
  embedding_dim: 512
  cors_origins:
    - http://localhost:5173

bot:
  token: "YOUR_BOT_TOKEN"
  backend_url: http://localhost:8000

frontend:
  default_limit: 20
Parameters explained:

database_url – PostgreSQL connection string.

redis_host/port – Redis server location.

n_clusters – Number of embedding clusters per track/user.

num_people_refilter – How many top text‑matched users to rerank by music.

admin_password – Password to claim admin rights in Telegram.

faiss_index_path – Where to persist the FAISS index.

embedding_dim – Dimensionality of CLMR embeddings (usually 512).

cors_origins – Allowed origins for the web dashboard.

bot.token – Telegram bot token.

bot.backend_url – Internal URL for bot to reach backend API.

frontend.default_limit – Default number of recommendations to show.
Usage
Telegram Bot
Start the bot with /start to register.

Use the main menu buttons:

Answer Polls – complete active polls.

Show Rankings – see your personalized recommendations.

Request Admin – enter admin password to unlock admin panel.

Admin panel allows creating new polls and viewing reports.

Web Dashboard
Login via Telegram widget (or simply enter your Telegram ID for demo).

View your recommendations and global leaderboard.

Admin users see an "Admin" link to manage polls and groups.

LLM Council Integration (Optional)
See prompts/llm_council_installation.md for instructions on setting up the LLM Council tool, which can be used independently for generating insights or explanations.

Testing
Run backend tests:

bash
cd backend
pytest
Run frontend tests (if any):

bash
cd frontend/web
npm test
Contributing
Please read CONTRIBUTING.md for guidelines.

License
MIT

text

---

## **7. Create_Presenation.md**

This file outlines a presentation structure for showcasing the project.

```markdown
# Project Presentation Outline

## Title Slide
- Project Name: SoundMatchBot
- Your Name / Team
- Date

## Problem Statement
- People with similar music tastes often don't know each other.
- Existing recommendation systems focus on songs, not people.

## Solution
- A Telegram bot + web dashboard that matches users based on music taste.
- Uses poll answers and actual music embeddings from YouTube.

## Architecture Overview
- Backend: FastAPI, PostgreSQL, FAISS, Redis
- Frontend: Telegram Bot (python-telegram-bot) + React/Vite
- Music Embeddings: CLMR model

## Key Features
- User registration via Telegram
- Admin‑created polls
- Two‑stage matching: text then music
- Fast leaderboard with Redis cache
- Configurable via single YAML

## Demo
- Show Telegram bot interaction (start, answer poll, view rankings)
- Show web dashboard (rankings, admin panel)
- Explain how matching works with a simple example

## Technical Deep Dive
- Embedding extraction pipeline (YouTube → CLMR → FAISS)
- Matching algorithm: text filter (TF‑IDF) + music rerank (cosine similarity)
- Database schema
- Caching strategy

## Configuration and Deployment
- Single config.yaml
- Docker Compose for easy deployment (optional)

## Challenges and Solutions
- Handling slow embedding extraction → background tasks
- Real‑time updates → Redis
- Ensuring privacy → only share anonymized rankings

## Future Work
- Integration with Spotify API
- Group chats based on matched users
- LLM‑generated explanations for recommendations

## Q&A
