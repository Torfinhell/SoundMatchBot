# SoundMatchBot

Match with users based on music taste and poll compatibility.

## Setup

1. **Database**: parameters in `config.yaml` require a running PostgreSQL (db: `soundmatch`) and Redis.
2. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m scripts.init_db
   uvicorn main:app --reload
   ```
3. **Telegram Bot**:
   ```bash
   cd frontend/telegram_bot
   pip install -r requirements.txt
   python main.py
   ```
4. **Web Dashboard**:
   ```bash
   cd frontend/web
   npm install
   npm run dev
   ```
