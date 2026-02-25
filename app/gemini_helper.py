import os
from typing import List, Dict, Any, Optional

try:
    import google.generativeai as genai
except Exception:
    genai = None


MODEL_NAME = "gemini-1.5-flash"


def _init() -> Optional["genai.GenerativeModel"]:
    api_key = os.getenv("GEMINI_API_KEY")
    if genai is None or not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)


def summarize(user: Dict[str, Any], schemes: List[Dict[str, Any]]) -> Optional[str]:
    """
    Returns a concise, friendly summary or None if Gemini not configured.
    """
    model = _init()
    if not model or not schemes:
        return None

    # Keep prompt short and deterministic for hackathons
    prompt = f"""
You are Yojna Mitra, a helpful assistant for Indian government schemes.
User profile: {user}
Matched schemes (JSON): {schemes}

Task:
- Recommend up to the best 3 schemes.
- For each, explain in 1–2 lines why it fits (age, income, gender/state if applicable).
- Keep it concise, bullet points, plain text.
"""

    try:
        resp = model.generate_content(prompt)
        text = (resp.text or "").strip()
        return text if text else None
    except Exception:
        return None