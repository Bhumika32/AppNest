class ModuleExecutor:
    module_key = None

    def execute(self, payload: dict, user):
        """
        Executes module logic only.
        Must NOT handle:
        - XP
        - analytics
        - notifications
        - database commits unrelated to module result
        """
        raise NotImplementedError

    def safe_execute(self, payload: dict, user) -> dict:
        """
        Executes module safely without crashing the system.
        """
        try:
            return self.execute(payload, user)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e),
                "is_complete": True
            }
