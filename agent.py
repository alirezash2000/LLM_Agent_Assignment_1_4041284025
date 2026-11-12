import ollama
from prompts import PLANNER_PROMPT, SOLVER_PROMPT, VERIFIER_PROMPT
from utils import strip_thinking_and_markdown, extract_clean_answer


class LocalReasoningAgent:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def _generate(self, prompt: str, temperature: float = 0.0) -> str:
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise logical and mathematical reasoning AI. Follow instructions strictly.",
                    },
                    {"role": "user", "content": prompt},
                ],
                options={
                    "temperature": temperature,
                    "num_predict": 2048,
                },
            )
            if isinstance(response, dict):
                return response.get("message", {}).get("content", "")
            return response.message.content
        except Exception as e:
            return f"LLM_ERROR: {str(e)}"

    def solve_problem(self, problem_text: str) -> str:
        if not problem_text or not str(problem_text).strip():
            return ""

        plan_prompt = PLANNER_PROMPT.format(problem=problem_text)
        raw_plan = self._generate(plan_prompt, temperature=0.1)
        clean_plan = strip_thinking_and_markdown(raw_plan)

        solver_prompt = SOLVER_PROMPT.format(problem=problem_text, plan=clean_plan)
        raw_solution = self._generate(solver_prompt, temperature=0.1)
        clean_solution = strip_thinking_and_markdown(raw_solution)

        verifier_prompt = VERIFIER_PROMPT.format(
            problem=problem_text,
            plan=clean_plan,
            solution=clean_solution,
        )
        raw_verified = self._generate(verifier_prompt, temperature=0.0)
        final_answer = extract_clean_answer(raw_verified)

        if not final_answer or "LLM_ERROR" in final_answer:
            fallback_prompt = (
                f"Solve the following problem carefully and output ONLY the final answer "
                f"inside <ANSWER></ANSWER> tags without any extra words:\n\n{problem_text}"
            )
            raw_fallback = self._generate(fallback_prompt, temperature=0.0)
            final_answer = extract_clean_answer(raw_fallback)

        return final_answer
