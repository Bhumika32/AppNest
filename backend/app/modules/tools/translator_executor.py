from app.platform.module_executor import ModuleExecutor
from app.platform.module_result import ModuleResult

class TranslatorExecutor(ModuleExecutor):
    """
    Simple translator executor.
    This integrates with the AppNest module system using module_key.
    """

    module_key = "translator"

    def execute(self, payload, user) -> ModuleResult:
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

        # Temporary demo translation logic
        # (later you can replace with real API)
        translated_text = f"[{target}] {text}"

        return ModuleResult(
            completed=True,
            status="success",
            data={
                "original_text": text,
                "translated_text": translated_text,
                "target_language": target
            }
        )