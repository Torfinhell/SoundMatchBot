# LLM Council Installation Guide

This guide explains how to install and run the LLM Council tool separately. It is not required for the core project but can be used for generating insights or explanations.

## Prerequisites
- Python 3.10+
- `uv` package manager

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/karpathy/llm-council.git
   cd llm-council
Install dependencies with uv

bash
uv sync
Set up environment variables
Create a .env file in the project root:

text
OPENROUTER_API_KEY=sk-or-v1-...
Get your API key from openrouter.ai and add credits if needed.

Configure models
Edit backend/config.py (inside llm-council) to define the council members:

python
COUNCIL_MODELS = [
    "openai/gpt-5.1",
    "google/gemini-3-pro-preview",
    "anthropic/claude-sonnet-4.6",
    "x-ai/grok-4",
]
CHAIRMAN_MODEL = "google/gemini-3-pro-preview"
