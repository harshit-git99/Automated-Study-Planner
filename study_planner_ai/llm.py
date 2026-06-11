import os
from typing import Any, Dict, Optional

from openai import OpenAI


class LLMClient:
    def __init__(self, model: Optional[str] = None):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Set it using the instructions in README.md."
            )

        # openai>=1.0.0
        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate_study_plan(self, prompt: str, *, temperature: float = 0.4) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert study coach. Create an actionable day-wise plan. "
                        "Keep it concise, realistic, and burnout-aware. "
                        "Output in a human-readable format with headings per day."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        return (resp.choices[0].message.content or "").strip()

