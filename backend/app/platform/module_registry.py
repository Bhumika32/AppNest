import importlib
import pkgutil
import inspect
from app.platform.module_executor import ModuleExecutor

class ModuleRegistry:
    _registry = {}
    _discovered = False

    @classmethod
    def _discover_modules(cls):
        if cls._discovered:
            return
            
        packages = ["app.services.tools", "app.services.games"]
        
        for package_name in packages:
            try:
                package = importlib.import_module(package_name)
                # Ensure the path is a list if it only has one element
                paths = getattr(package, '__path__', [])
                for _, module_name, _ in pkgutil.iter_modules(paths):
                    full_module_name = f"{package_name}.{module_name}"
                    module = importlib.import_module(full_module_name)
                    
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, ModuleExecutor) and obj is not ModuleExecutor:
                            if hasattr(obj, 'module_key') and obj.module_key:
                                cls._registry[obj.module_key] = obj()
            except Exception as e:
                import logging
                logging.warning(f"Failed to auto-discover {package_name}: {e}")
                
        cls._discovered = True

    @classmethod
    def register_executor(cls, key, executor_cls):
        cls._registry[key] = executor_cls()

    @classmethod
    def get_executor(cls, key):
        cls._discover_modules()
        if key not in cls._registry:
            raise Exception(f"No executor registered for {key}")
        return cls._registry[key]

# Forward exports for backward compatibility
registry = ModuleRegistry._registry
register_executor = ModuleRegistry.register_executor
get_executor = ModuleRegistry.get_executor
