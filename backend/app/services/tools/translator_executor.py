# backend/app/services/tools/translator_executor.py
from app.platform.module_executor import ModuleExecutor

class TranslatorExecutor(ModuleExecutor):
    """
    Simple translator executor.
    This integrates with the AppNest module system using module_key.
    """

    module_key = "translator"

    def execute(self, payload, user):
        metadata = payload.get("metadata", {})

        text = metadata.get("text")
        target = metadata.get("target")

        # validation
        if not text or not target:
            return {
                "error": "INVALID_INPUT",
                "message": "text and target language are required"
            }

        # Temporary demo translation logic
        # (later you can replace with real API)
        translated_text = f"[{target}] {text}"

        return {
            "original_text": text,
            "translated_text": translated_text,
            "target_language": target
        }