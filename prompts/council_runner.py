"""
Script to run LLM Council with custom prompt and model names.
Based on the setup from prompts/llm_council.md
"""

import sys
import os
import asyncio
from typing import List, Tuple, Dict, Any

# Add the llm-council directory to the path
llm_council_path = os.path.join(os.path.dirname(__file__), '..', 'llm-council')
sys.path.insert(0, llm_council_path)

from backend.config import COUNCIL_MODELS
from backend.council import run_full_council


def run_llm_council(prompt: str, model_names: List[str]) -> Tuple[List, List, Dict, Dict]:
    """
    Run the LLM Council with a custom prompt and list of model names.

    Args:
        prompt: The user's question or prompt to send to the council
        model_names: List of OpenRouter model identifiers to use as council members

    Returns:
        Tuple containing:
        - stage1_results: List of individual model responses
        - stage2_results: List of model rankings
        - stage3_result: Final synthesized answer from chairman
        - metadata: Additional info including rankings and mappings

    This function temporarily overrides the COUNCIL_MODELS config to use the provided models,
    runs the full 3-stage council process, then restores the original config.
    """
    # Store original models
    original_models = COUNCIL_MODELS[:]

    try:
        # Temporarily set the council models
        COUNCIL_MODELS.clear()
        COUNCIL_MODELS.extend(model_names)

        # Run the council process
        result = asyncio.run(run_full_council(prompt))

        return result

    finally:
        # Always restore original models
        COUNCIL_MODELS.clear()
        COUNCIL_MODELS.extend(original_models)


if __name__ == "__main__":
    # Example usage when run as a script
    #python prompts/council_runner.py "What is AI?" --models openai/gpt-4o google/gemini-pro-1.5 --files file1.txt file2.md
    import argparse

    parser = argparse.ArgumentParser(description="Run LLM Council with custom models")
    parser.add_argument("prompt", help="The prompt/question to send to the council")
    parser.add_argument("--models", nargs="+", required=True,
                       help="List of model names (e.g., openai/gpt-4o google/gemini-pro-1.5)")
    parser.add_argument("--files", nargs="*", default=[],
                       help="Optional files to include as context in the prompt")

    args = parser.parse_args()

    # Build the full prompt with file contents
    full_prompt = args.prompt
    if args.files:
        context_parts = []
        for file_path in args.files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    context_parts.append(f"Content from {file_path}:\n{content}")
            except Exception as e:
                print(f"Error: Could not read file {file_path}: {e}")
                sys.exit(1)
        
        if context_parts:
            context_text = "\n\n".join(context_parts)
            full_prompt = f"{context_text}\n\nQuestion: {args.prompt}"

    print(f"Running council with prompt: {args.prompt}")
    if args.files:
        print(f"Including context from files: {args.files}")
    print(f"Using models: {args.models}")

    try:
        stage1, stage2, stage3, metadata = run_llm_council(full_prompt, args.models)

        print("\n=== Stage 1: Individual Responses ===")
        for result in stage1:
            print(f"Model: {result['model']}")
            print(f"Response: {result['response'][:200]}...")
            print()

        print("=== Stage 2: Rankings ===")
        for result in stage2:
            print(f"Model: {result['model']}")
            print(f"Ranking: {result['ranking'][:200]}...")
            print()

        print("=== Stage 3: Final Answer ===")
        print(f"Chairman: {stage3['model']}")
        print(f"Response: {stage3['response']}")

        if metadata.get('aggregate_rankings'):
            print("\n=== Aggregate Rankings ===")
            for rank in metadata['aggregate_rankings']:
                print(f"{rank['model']}: {rank['average_rank']} (from {rank['rankings_count']} rankings)")

    except Exception as e:
        print(f"Error running council: {e}")
        sys.exit(1)