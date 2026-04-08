from app.platform.module_executor import ModuleExecutor
from app.platform.module_result import ModuleResult
import logging
logger = logging.getLogger(__name__)

class TranslatorExecutor(ModuleExecutor):
    """
    Simple translator executor.
    This integrates with the AppNest module system using module_key.
    """

    module_key = "TranslatorTool"

    def execute(self, payload, user) -> ModuleResult:
        logger.info(f"Executing Translator tool for user: {user.id}")
        metadata = payload.get("metadata", {})

        text = metadata.get("text")
        target = metadata.get("target")

        # validation
        if not text or not target:
            return ModuleResult(
                completed=False,
                status="error",
                error="INVALID_INPUT",
                message="text and target language are required"
            )

        # Temporary demo translation logic (Reverse string for decrypter simulation)
        translated_text = str(text)[::-1]

        return ModuleResult(
            completed=True,
            status="success",
            data={
                "original_text": text,
                "translated_text": translated_text,
                "target_language": target
            }
        )