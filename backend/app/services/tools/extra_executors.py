from app.platform.module_executor import ModuleExecutor

class CGPAExecutor(ModuleExecutor):
    module_key = "cgpa"

    def execute(self, payload: dict, user):
        metadata = payload.get("metadata", {})
        cgpa = metadata.get("cgpa")
        total_credits = metadata.get("totalCredits")
        
        return {
            "cgpa": cgpa,
            "total_credits": total_credits,
            "message": f"Academic processing complete. GPA set to {cgpa}"
        }

class JokeExecutor(ModuleExecutor):
    module_key = "joke"

    def execute(self, payload: dict, user):
        # Jokes are usually finalized on frontend for now to keep it responsive
        metadata = payload.get("metadata", {})
        return {
            "humor_status": "synced",
            "type": metadata.get("jokeType", "general")
        }

class TranslatorExecutor(ModuleExecutor):
    module_key = "translator"

    def execute(self, payload: dict, user):
        metadata = payload.get("metadata", {})
        return {
            "source_lang": metadata.get("from", "en"),
            "target_lang": metadata.get("to", "es"),
            "char_count": metadata.get("charCount", 0),
            "status": "decrypted"
        }
