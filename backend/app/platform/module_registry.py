class ModuleRegistry:
    _registry = {}

    @classmethod
    def register_executor(cls, key, executor_cls):
        cls._registry[key] = executor_cls()

    @classmethod
    def get_executor(cls, key):
        if key not in cls._registry:
            raise Exception(f"No executor registered for {key}")
        return cls._registry[key]

# Forward exports for backward compatibility
registry = ModuleRegistry._registry
register_executor = ModuleRegistry.register_executor
get_executor = ModuleRegistry.get_executor
