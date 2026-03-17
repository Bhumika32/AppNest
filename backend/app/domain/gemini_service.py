# -----------------------------------------------------------------------------
# File: backend/app/domain/gemini_service.py
#
# Description:
# Centralized AI service for AppNest.
#
# Responsibilities:
# - Handle all Gemini API interactions
# - Prevent duplicate AI calls
# - Generate roast + mentor advice in a single request
# - Safely parse Gemini responses
# - Ensure system stability if AI fails
#
# Stability Features:
# - Handles invalid JSON responses
# - Strips markdown formatting from Gemini output
# - Prevents crashes if AI fails
# -----------------------------------------------------------------------------

import logging
import json
import re

from google import genai
from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiService:

    def __init__(self):

        self.api_key = settings.GEMINI_API_KEY
        self.client = None

        if self.api_key:

            try:

                self.client = genai.Client(api_key=self.api_key)

                logger.info("Gemini AI initialized")

            except Exception as e:

                logger.error(f"Gemini client initialization failed: {e}")

        else:

            logger.warning("Gemini API Key missing. AI disabled.")

    # -------------------------------------------------------------------------
    # CLEAN GEMINI RESPONSE
    # -------------------------------------------------------------------------
    def _extract_json(self, text: str):

        if not text:
            return None

        try:
            return json.loads(text)
        except Exception:
            pass

        # Try to remove markdown code blocks
        try:

            cleaned = re.sub(r"```json|```", "", text).strip()

            return json.loads(cleaned)

        except Exception:
            pass

        # Try extracting JSON substring
        try:

            start = text.find("{")
            end = text.rfind("}") + 1

            if start != -1 and end != -1:

                substring = text[start:end]

                return json.loads(substring)

        except Exception:
            pass

        return None

    # -------------------------------------------------------------------------
    # SINGLE AI FEEDBACK CALL
    # -------------------------------------------------------------------------
    def generate_feedback(self, context: str):

        if not self.client:

            return {
                "roast": None,
                "mentor": None
            }

        prompt = f"""
You are AppNest's AI game administrator.

Based on this context:

{context}

Generate:

1) A sarcastic roast (max 12 words)
2) A helpful mentor tip (max 12 words)

Return JSON only:

{{
 "roast": "...",
 "mentor": "..."
}}
"""

        try:

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            text = response.text.strip()

            data = self._extract_json(text)

            if not data:

                logger.warning("Gemini returned invalid JSON")

                return {
                    "roast": None,
                    "mentor": None
                }

            return {
                "roast": data.get("roast"),
                "mentor": data.get("mentor")
            }

        except Exception as e:

            logger.error(f"Gemini feedback generation failed: {e}")

            return {
                "roast": None,
                "mentor": None
            }


gemini_ai = GeminiService()