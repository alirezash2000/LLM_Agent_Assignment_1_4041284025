import argparse
import json
import os
import sys
from agent import LocalReasoningAgent
from utils import select_model


def process_data(data, agent: LocalReasoningAgent):
    if isinstance(data, dict):
        if "problem" in data:
            problem_id = data.get("id", "test_001")
            problem_text = data.get("problem", "")
            answer = agent.solve_problem(problem_text)
            return {
                "id": problem_id,
                "answer": str(answer),
            }
        for key in ("problems", "questions", "data", "items"):
            if key in data and isinstance(data[key], list):
                return {
                    key: [
                        {
                            "id": item.get("id", f"test_{idx+1:03d}"),
                            "answer": str(agent.solve_problem(item.get("problem", ""))),
                        }
                        for idx, item in enumerate(data[key])
                    ]
                }

    if isinstance(data, list):
        results = []
        for idx, item in enumerate(data):
            if isinstance(item, dict):
                problem_id = item.get("id", f"test_{idx+1:03d}")
                problem_text = item.get("problem", "")
                answer = agent.solve_problem(problem_text)
                results.append({
                    "id": problem_id,
                    "answer": str(answer),
                })
        return results

    raise ValueError("Unsupported input JSON structure.")


def main():
    parser = argparse.ArgumentParser(description="LLM Agent for Local Multi-Step Reasoning")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--output", required=True, help="Path to output JSON file")
    parser.add_argument(
        "--model",
        default=os.environ.get("OLLAMA_MODEL", "qwen3:8b"),
        help="Preferred Ollama model name",
    )
    args = parser.parse_args()

    active_model = select_model(args.model)
    agent = LocalReasoningAgent(model_name=active_model)

    try:
        with open(args.input, "r", encoding="utf-8") as infile:
            input_data = json.load(infile)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        output_data = process_data(input_data, agent)
    except Exception as e:
        print(f"Error processing problems: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        output_dir = os.path.dirname(os.path.abspath(args.output))
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as outfile:
            json.dump(output_data, outfile, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
