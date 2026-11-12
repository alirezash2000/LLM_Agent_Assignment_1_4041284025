import re
import ollama


def select_model(preferred_model: str = "qwen3:8b") -> str:
    try:
        response = ollama.list()
        installed_models = []

        if hasattr(response, "models"):
            installed_models = [m.model for m in response.models]
        elif isinstance(response, dict) and "models" in response:
            installed_models = [m.get("name") or m.get("model") for m in response["models"]]

        if not installed_models:
            return preferred_model

        if preferred_model in installed_models:
            return preferred_model

        base_preferred = preferred_model.split(":")[0].lower()
        for m in installed_models:
            if m.lower().startswith(base_preferred):
                return m

        for m in installed_models:
            if "qwen2.5" in m.lower() or "qwen" in m.lower():
                return m

        return installed_models[0]
    except Exception:
        return preferred_model


def strip_thinking_and_markdown(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    cleaned = cleaned.replace("```json", "").replace("```text", "").replace("```", "").replace("**", "")
    return cleaned.strip()


def extract_clean_answer(raw_text: str) -> str:
    cleaned = strip_thinking_and_markdown(raw_text)

    matches = re.findall(r"<ANSWER>(.*?)</ANSWER>", cleaned, flags=re.DOTALL | re.IGNORECASE)
    if matches:
        ans = matches[-1].strip()
    else:
        lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
        ans = lines[-1] if lines else ""

    ans = re.sub(
        r"^(Final Answer|Answer|Output|Result|پاسخ نهایی|پاسخ|جواب)\s*[:\-=]\s*",
        "",
        ans,
        flags=re.IGNORECASE,
    ).strip()

    if (ans.startswith('"') and ans.endswith('"')) or (ans.startswith("'") and ans.endswith("'")):
        ans = ans[1:-1].strip()
    if ans.startswith("<") and ans.endswith(">"):
        ans = ans[1:-1].strip()

    if ans.endswith(".") and len(ans.split()) <= 5:
        ans = ans[:-1].strip()

    return ans
