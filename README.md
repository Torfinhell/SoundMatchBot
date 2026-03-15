# SoundMatchBot

A comprehensive music-based social matching platform that connects users based on music taste and poll compatibility. Built with FastAPI backend, Telegram bot, and React web dashboard.

## Features

- **User Registration**: Telegram-based user onboarding
- **Music Taste Analysis**: CLMR-powered audio feature extraction
- **Poll System**: Admin-created polls for compatibility matching
- **Two-Phase Matching**: Text-based filtering + music-based reranking
- **Real-time Leaderboard**: Global rankings via web dashboard
- **Admin Panel**: Poll creation and user management

## Prerequisites

- **Python 3.10+**
- **PostgreSQL** database
- **Redis** server
- **Node.js 16+** (for web dashboard)
- **Telegram Bot Token** (from @BotFather)

## Quick Setup

### 1. Clone and Environment Setup

```bash
git clone <repository-url>
cd SoundMatchBot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# If you get "externally-managed-environment" error, use:
# python3 -m venv --system-site-packages venv
```

### 2. Database Setup

```bash
# Install PostgreSQL and Redis (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib redis-server

# Create database
sudo -u postgres createdb soundmatch
sudo -u postgres psql -c "CREATE USER soundmatch_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE soundmatch TO soundmatch_user;"

# Start Redis
sudo systemctl start redis-server
```

### 3. Configuration

Edit `config.yaml`:

```yaml
backend:
  database_url: postgresql://soundmatch_user:your_password@localhost:5432/soundmatch
  redis_host: localhost
  redis_port: 6379
  admin_password: "your_secure_admin_password"
  # ... other settings

bot:
  token: "YOUR_TELEGRAM_BOT_TOKEN"
  # ... 

frontend:
  # ...
```

### 4. Requirements Check

Run the automated requirements checker:

```bash
python check_requirements.py
```

This will verify your Python version, dependencies, database connections, and configuration.

### 4. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt
```

Or run directly from project root:

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Initialize database
python -m backend.scripts.init_db

# Run server
python run_backend.py
```

### 5. Telegram Bot Setup

```bash
cd ../frontend/telegram_bot

# Install dependencies
pip install -r requirements.txt

# Run bot (in separate terminal)
python main.py
```

### 6. Web Dashboard Setup

```bash
cd ../frontend/web

# Install dependencies
npm install

# Run development server
npm run dev
```

## API Documentation

Once the backend is running, visit:
- **API Docs**: http://localhost:8000/docs
- **Web Dashboard**: http://localhost:5173
- **Bot**: Start a chat with your bot on Telegram

## Project Structure

```
SoundMatchBot/
├── config.yaml              # Shared configuration
├── backend/                 # FastAPI application
│   ├── main.py             # Application entry point
│   ├── config.py           # Settings management
│   ├── database.py         # Database connection
│   ├── models.py           # SQLAlchemy models
│   ├── faiss_index.py      # Vector search index
│   ├── requirements.txt    # Python dependencies
│   ├── routers/            # API endpoints
│   │   ├── users.py
│   │   ├── polls.py
│   │   ├── admin.py
│   │   └── recommendations.py
│   ├── services/           # Business logic
│   │   ├── matching.py
│   │   ├── embedding.py    # CLMR feature extraction
│   │   └── ranking.py
│   └── scripts/            # Utility scripts
│       └── init_db.py
├── frontend/
│   ├── telegram_bot/       # Telegram bot
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api_client.py
│   │   └── handlers/
│   └── web/                # React dashboard
│       ├── src/
│       ├── package.json
│       └── vite.config.ts
├── sample_notebooks/       # Feature extraction examples
└── prompts/                # LLM Council prompts
```

## Troubleshooting

### Common Issues

**1. "externally-managed-environment" Error**
```bash
# This happens on some Linux distributions with system Python
# Solution 1: Use a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Solution 2: Use --break-system-packages (not recommended)
pip install -r requirements.txt --break-system-packages

# Solution 3: Use pipx for applications
pipx install fastapi uvicorn  # Install globally
```

**2. Database Connection Error**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify connection
psql -h localhost -U soundmatch_user -d soundmatch
```

**3. Redis Connection Error**
```bash
# Check Redis is running
sudo systemctl status redis-server

# Test connection
redis-cli ping
```

**4. Import Errors in Scripts**
```bash
# Use the run script which handles paths correctly
python run_backend.py

# Or run from backend directory
cd backend
python -m scripts.init_db

# Or set PYTHONPATH manually
export PYTHONPATH=/path/to/SoundMatchBot:$PYTHONPATH
cd backend && python scripts/init_db.py
```

**5. Telegram Bot Not Responding**
- Verify bot token in `config.yaml`
- Check bot permissions in Telegram
- Ensure backend is running and accessible

**6. Web Dashboard Not Loading**
```bash
# Check Node.js version
node --version

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Development Commands

```bash
# Backend development
cd backend
uvicorn main:app --reload --log-level info

# Database migrations (if needed)
alembic revision --autogenerate -m "Add new table"
alembic upgrade head

# Frontend development
cd frontend/web
npm run build  # Production build
npm run preview  # Preview production build
```

## Deployment

### Docker Deployment (Recommended)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Deployment

- Use Gunicorn for production server
- Set up reverse proxy (nginx)
- Configure environment variables
- Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the maintainers.
