"""
app/tools/moodfix/gemini_client.py

Gemini Client (NEW SDK ✅ google.genai)

✅ Uses environment variable: GEMINI_API_KEY
✅ Prints errors clearly in terminal
✅ One job: return text from Gemini
"""

import os

from google import genai


class GeminiClient:
    @staticmethod
    def generate_text(prompt: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing in environment.")

        # ✅ Create client
        client = genai.Client(api_key=api_key)

        # ✅ Choose a safe default model
        # If this model fails, change it to another available one.
        model = "gemini-1.5-flash"

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            # ✅ genai response text
            text = getattr(response, "text", None)
            if not text:
                raise RuntimeError("Gemini returned empty response.")
            return text

        except Exception as e:
            print(f"❌ Gemini error: {e}")
            raise RuntimeError(f"Gemini API error: {e}")