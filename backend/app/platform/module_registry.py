# -----------------------------------------------------------------------------
# File: backend/app/platform/module_registry.py
#
# Description:
# Dynamic registry for AppNest module executors.
#
# Responsibilities:
# - Auto-discover executors in tools and games packages
# - Validate module executor structure
# - Prevent duplicate module_key registration
# - Provide executor instances per request
#
# Stability Improvements:
# - Thread-safe module discovery
# - Strict duplicate detection
# - Improved logging
# - Executor validation
# -----------------------------------------------------------------------------

import importlib
import pkgutil
import inspect
import logging
import threading

from app.platform.module_executor import ModuleExecutor

logger = logging.getLogger(__name__)


class ModuleRegistry:

    _registry = {}
    _discovered = False
    _lock = threading.Lock()

    # -------------------------------------------------------------------------
    # MODULE DISCOVERY
    # -------------------------------------------------------------------------
    @classmethod
    def _discover_modules(cls):

        if cls._discovered:
            return

        with cls._lock:

            if cls._discovered:
                return

            packages = [
                "app.modules.tools",
                "app.modules.games"
            ]

            for package_name in packages:

                try:

                    package = importlib.import_module(package_name)

                    paths = getattr(package, "__path__", [])

                    for _, module_name, _ in pkgutil.iter_modules(paths):

                        full_module_name = f"{package_name}.{module_name}"

                        try:

                            module = importlib.import_module(full_module_name)

                            for _, obj in inspect.getmembers(module, inspect.isclass):

                                if not issubclass(obj, ModuleExecutor):
                                    continue

                                if obj is ModuleExecutor:
                                    continue

                                module_key = getattr(obj, "module_key", None)

                                if not module_key or not isinstance(module_key, str):

                                    raise RuntimeError(
                                        f"{obj.__name__} missing valid module_key"
                                    )

                                if module_key in cls._registry:

                                    raise RuntimeError(
                                        f"Duplicate module_key detected: {module_key}"
                                    )

                                cls._registry[module_key] = obj

                                logger.info(
                                    f"[ModuleRegistry] Registered executor: {module_key}"
                                )

                        except Exception:

                            logger.exception(
                                f"[ModuleRegistry] Failed loading module {full_module_name}"
                            )

                except Exception:

                    logger.exception(
                        f"[ModuleRegistry] Failed discovering package {package_name}"
                    )

            cls._discovered = True

    # -------------------------------------------------------------------------
    # MANUAL REGISTRATION
    # -------------------------------------------------------------------------
    @classmethod
    def register_executor(cls, key, executor_cls):

        if not key or not isinstance(key, str):

            raise ValueError("Executor key must be a valid string")

        if not issubclass(executor_cls, ModuleExecutor):

            raise TypeError("Executor must inherit from ModuleExecutor")

        if key in cls._registry:

            raise RuntimeError(f"Executor already registered for key: {key}")

        cls._registry[key] = executor_cls

        logger.info(f"[ModuleRegistry] Manually registered executor: {key}")

    # -------------------------------------------------------------------------
    # EXECUTOR RETRIEVAL
    # -------------------------------------------------------------------------
    @classmethod
    def get_executor(cls, key):

        cls._discover_modules()

        executor_cls = cls._registry.get(key)

        if not executor_cls:

            raise RuntimeError(f"No executor registered for module: {key}")

        return executor_cls()


# -------------------------------------------------------------------------
# BACKWARD COMPATIBILITY EXPORTS
# -------------------------------------------------------------------------
registry = ModuleRegistry._registry
register_executor = ModuleRegistry.register_executor
get_executor = ModuleRegistry.get_executor
# import importlib
# import pkgutil
# import inspect
# from app.platform.module_executor import ModuleExecutor

# class ModuleRegistry:
#     _registry = {}
#     _discovered = False

#     @classmethod
#     def _discover_modules(cls):
#         if cls._discovered:
#             return
            
#         packages = ["app.modules.tools", "app.modules.games"]
        
#         for package_name in packages:
#             try:
#                 package = importlib.import_module(package_name)
#                 # Ensure the path is a list if it only has one element
#                 paths = getattr(package, '__path__', [])
#                 for _, module_name, _ in pkgutil.iter_modules(paths):
#                     full_module_name = f"{package_name}.{module_name}"
#                     module = importlib.import_module(full_module_name)
                    
#                     for name, obj in inspect.getmembers(module, inspect.isclass):
#                         if issubclass(obj, ModuleExecutor) and obj is not ModuleExecutor:
#                             if hasattr(obj, 'module_key') and obj.module_key:
#                                 if obj.module_key in cls._registry:
#                                     import logging
#                                     logging.warning(f"Duplicate registration detected for module_key: {obj.module_key}. Skipping {full_module_name}")
#                                     continue
#                                 cls._registry[obj.module_key] = obj()
#             except Exception as e:
#                 import logging
#                 logging.warning(f"Failed to auto-discover {package_name}: {e}")
                
#         cls._discovered = True

#     @classmethod
#     def register_executor(cls, key, executor_cls):
#         cls._registry[key] = executor_cls()

#     @classmethod
#     def get_executor(cls, key):
#         cls._discover_modules()
#         if key not in cls._registry:
#             raise Exception(f"No executor registered for {key}")
#         return cls._registry[key]

# # Forward exports for backward compatibility
# registry = ModuleRegistry._registry
# register_executor = ModuleRegistry.register_executor
# get_executor = ModuleRegistry.get_executor
