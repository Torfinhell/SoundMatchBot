First I need you to set LLM council up for me using this: 
1. Install Dependencies
The project uses uv for project management.

Backend:

uv sync
Frontend:

cd frontend
npm install
cd ..
2. Configure API Key
Create a .env file in the project root:
OPENROUTER_API_KEY=sk-or-v1-...
Get your API key at openrouter.ai. Make sure to purchase the credits you need, or sign up for automatic top up.
The repository is taken from https://github.com/karpathy/llm-council.git
and then:
3. Configure Models 
Edit backend/config.py to customize the council:

COUNCIL_MODELS = [
    "openai/gpt-5.1",
    "google/gemini-3-pro-preview",
    "anthropic/claude-sonnet-4.6",
    "x-ai/grok-4",
]

CHAIRMAN_MODEL = "google/gemini-3-pro-preview"

To run the application(dont do if not asked)
Running the Application
Option 1: Use the start script

./start.sh
Option 2: Run manually

Terminal 1 (Backend):

uv run python -m backend.main
Terminal 2 (Frontend):

cd frontend
npm run dev
Then open http://localhost:5173 in your browser.

