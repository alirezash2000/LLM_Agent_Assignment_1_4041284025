# LLM_Agent_Assignment_1_4041284025
# Local Reasoning LLM Agent (Assignment 1)

This project implements a multi-step local reasoning Agent powered by Ollama to solve logical, mathematical, scheduling, and constraint-satisfaction problems completely offline.

## Agent Architecture

The system employs a three-stage Plan-Solve-Verify architecture within the `LocalReasoningAgent` class:

1. **Planner (`PLANNER_PROMPT`)**: Analyzes the problem statement, identifies its category, extracts all explicit and implicit variables and constraints, and determines the exact target output format.
2. **Solver (`SOLVER_PROMPT`)**: Uses the extracted constraints from the first stage to solve the problem systematically through step-by-step Chain-of-Thought (CoT) reasoning.
3. **Verifier (`VERIFIER_PROMPT`)**: Cross-checks the proposed solution against all constraints, corrects any calculation or logical errors, and places the final formatted answer inside `<ANSWER>...</ANSWER>` tags.

Post-processing functions in `utils.py` strip internal thinking tags and Markdown formatting so that only the exact final answer is saved to the output file. Additionally, `select_model` defaults to `qwen3:8b` and automatically falls back to any available local Ollama model if the default model is not installed.

## Project Structure

- `main.py`: Main entry point, CLI argument parser, and JSON input/output handler.
- `agent.py`: Implementation of `LocalReasoningAgent`, the three-stage reasoning pipeline, and the fallback mechanism.
- `prompts.py`: Structured prompt templates for the Planner, Solver, and Verifier stages.
- `utils.py`: Helper functions for automatic model selection and final answer extraction and cleaning.
- `requirements.txt`: Python package dependencies.
- `README.md`: Project documentation, setup, and usage instructions.

## Installation

1. Verify that Ollama is installed and running:

```bash
ollama --version
```

2. Pull the required language model in Ollama:

```bash
ollama pull qwen3:8b
```

3. Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the program offline using the standard command-line interface:

```bash
python main.py --input input.json --output output.json
```

To specify a custom model name manually:

```bash
python main.py --input input.json --output output.json --model qwen3:8b
```

### Input Format (`input.json`)

```json
{
  "id": "test_001",
  "problem": "Problem description goes here."
}
```

### Output Format (`output.json`)

```json
{
  "id": "test_001",
  "answer": "FINAL ANSWER"
}
```
