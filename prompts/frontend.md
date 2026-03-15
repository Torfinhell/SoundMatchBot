4. frontend.md
This file details the Telegram bot and React web dashboard, including handlers, components, and their interactions.

markdown
# Frontend Architecture

The frontend consists of two parts:
1. **Telegram Bot** – built with `python-telegram-bot` (or `aiogram`), runs as a separate process interacting with the backend API.
2. **Web Dashboard** – React + Vite single‑page application, also communicating with the backend API.

Both share the same configuration (from `config.yaml`).

## Telegram Bot

### Folder Structure
frontend/
├── telegram_bot/
│ ├── main.py # Bot entry point
│ ├── handlers/
│ │ ├── start.py # /start command
│ │ ├── admin.py # Admin request and panel
│ │ ├── polls.py # Poll interaction
│ │ ├── ranking.py # Show ranking
│ │ └── common.py # Shared utilities
│ ├── keyboards.py # Inline keyboards
│ ├── callbacks.py # Callback query handlers
│ ├── config.py # Load bot‑specific settings
│ └── api_client.py # Async HTTP client for backend API

text

### Bot Features

#### `start.py`
- **Handler**: `/start`
- **Action**: Calls backend `POST /register` with `telegram_id` and `username`. Stores `user_id` in context. Sends welcome message with main menu buttons.

#### `admin.py`
- **Handler**: "Request Admin" button (callback data `admin_request`).
- **Flow**: Prompts user to enter admin password. Verifies via backend `POST /admin/claim`. If correct, sets user as admin in DB and shows admin panel.
- **Admin Panel**: Buttons: "Create Poll", "Manage Groups", "View Reports". Each triggers corresponding handlers.

#### `polls.py`
- **Handler**: "Answer Polls" button → shows list of active polls from backend `GET /polls/active`.
- **Poll Interaction**: For each poll, sends series of questions. Collects answers and submits via `POST /polls/{poll_id}/submit`.
- **Keyboard**: Inline buttons for answer options (if multiple choice) or text input.

#### `ranking.py`
- **Handler**: "Show Rankings" button → fetches `GET /recommendations/{user_id}` and displays formatted list (username + score). Possibly also "Global Leaderboard".

#### `keyboards.py`
Defines reusable inline keyboards:
- `main_menu_keyboard()` – Home, Polls, Rankings, Admin (if admin).
- `poll_navigation_keyboard()` – Next, Previous, Submit.
- `confirmation_keyboard()` – Yes/No.

#### `callbacks.py`
Processes callback data like `poll_answer_123`, `admin_confirm`, etc.

### Configuration (`config.py`)
Loads from `config.yaml` (shared with backend):
- `BOT_TOKEN` – Telegram bot token (should be in env or config).
- `BACKEND_URL` – base URL for API.
- `ADMIN_PASSWORD` – same as backend.
- `POLL_QUESTION_TYPES` – optional: mapping of question to input type.

### Running the Bot
```bash
cd frontend/telegram_bot
python main.py
Web Dashboard (React + Vite)
Folder Structure
text
frontend/web/
├── public/
├── src/
│   ├── components/
│   │   ├── Layout/
│   │   ├── Auth/               # Telegram auth simulation (if needed)
│   │   ├── Dashboard/
│   │   ├── Polls/
│   │   ├── Rankings/
│   │   └── Admin/
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Login.tsx            # Maybe Telegram widget
│   │   ├── Polls.tsx
│   │   ├── Rankings.tsx
│   │   └── AdminPanel.tsx
│   ├── services/
│   │   └── api.ts               # Axios instance for backend
│   ├── hooks/                    # Custom React hooks
│   ├── utils/
│   ├── App.tsx
│   ├── main.tsx
│   └── config.ts                 # Load from env/config.yaml
├── package.json
├── vite.config.ts
└── .env
Key Components
services/api.ts
Axios client with base URL from config.

Interceptors for error handling.

Functions: registerUser, getPolls, submitPoll, getRecommendations, claimAdmin, etc.

pages/Rankings.tsx
Displays current user's recommendations and global leaderboard.

Uses useEffect to fetch data on mount.

Styled with dark theme (black background, white text, accent colors).

pages/AdminPanel.tsx
Protected route; checks if user is admin via backend (stores admin status in context).

Forms to create polls, manage groups (future), view reports.

Poll creation form dynamically adds question fields.

components/Polls/PollQuestion.tsx
Renders a single poll question based on type (text, multiple choice, rating).

Collects answer and updates parent state.

components/Rankings/UserCard.tsx
Displays user info and similarity score.

Styling
CSS modules or Tailwind CSS.

Ensure black background, high contrast for readability.

Responsive design for mobile/desktop.