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

                                logger.debug(
                                    "Registered executor: %s", module_key
                                )

                        except Exception:

                            logger.exception(
                                "Failed loading module %s", full_module_name
                            )

                except Exception:

                    logger.exception(
                        "Failed discovering package %s", package_name
                    )

            cls._discovered = True

    @classmethod
    def register_executor(cls, key, executor_cls):

        if not key or not isinstance(key, str):
            raise ValueError("Executor key must be a valid string")

        if not issubclass(executor_cls, ModuleExecutor):
            raise TypeError("Executor must inherit from ModuleExecutor")

        if key in cls._registry:
            raise RuntimeError(f"Executor already registered for key: {key}")

        cls._registry[key] = executor_cls

        logger.info("Manually registered executor: %s", key)

    @classmethod
    def get_executor(cls, key):

        cls._discover_modules()

        executor_cls = cls._registry.get(key)

        if not executor_cls:
            raise KeyError(f"No executor registered for module: {key}")

        return executor_cls()


registry = ModuleRegistry._registry
register_executor = ModuleRegistry.register_executor
get_executor = ModuleRegistry.get_executor
# # -----------------------------------------------------------------------------
# # File: backend/app/platform/module_registry.py
# #
# # Description:
# # Dynamic registry for AppNest module executors.
# #
# # Responsibilities:
# # - Auto-discover executors in tools and games packages
# # - Validate module executor structure
# # - Prevent duplicate module_key registration
# # - Provide executor instances per request
# #
# # Stability Improvements:
# # - Thread-safe module discovery
# # - Strict duplicate detection
# # - Improved logging
# # - Executor validation
# # -----------------------------------------------------------------------------

# import importlib
# import pkgutil
# import inspect
# import logging
# import threading

# from app.platform.module_executor import ModuleExecutor

# logger = logging.getLogger(__name__)


# class ModuleRegistry:

#     _registry = {}
#     _discovered = False
#     _lock = threading.Lock()

#     # -------------------------------------------------------------------------
#     # MODULE DISCOVERY
#     # -------------------------------------------------------------------------
#     @classmethod
#     def _discover_modules(cls):

#         if cls._discovered:
#             return

#         with cls._lock:

#             if cls._discovered:
#                 return

#             packages = [
#                 "app.modules.tools",
#                 "app.modules.games"
#             ]

#             for package_name in packages:

#                 try:

#                     package = importlib.import_module(package_name)

#                     paths = getattr(package, "__path__", [])

#                     for _, module_name, _ in pkgutil.iter_modules(paths):

#                         full_module_name = f"{package_name}.{module_name}"

#                         try:

#                             module = importlib.import_module(full_module_name)

#                             for _, obj in inspect.getmembers(module, inspect.isclass):

#                                 if not issubclass(obj, ModuleExecutor):
#                                     continue

#                                 if obj is ModuleExecutor:
#                                     continue

#                                 module_key = getattr(obj, "module_key", None)

#                                 if not module_key or not isinstance(module_key, str):

#                                     raise RuntimeError(
#                                         f"{obj.__name__} missing valid module_key"
#                                     )

#                                 if module_key in cls._registry:

#                                     raise RuntimeError(
#                                         f"Duplicate module_key detected: {module_key}"
#                                     )

#                                 cls._registry[module_key] = obj

#                                 logger.debug(
#                                     "[ModuleRegistry] Registered executor: %s", module_key
#                                 )

#                         except Exception:

#                             logger.exception(
#                                 "[ModuleRegistry] Failed loading module %s", full_module_name
#                             )

#                 except Exception:

#                     logger.exception(
#                         "[ModuleRegistry] Failed discovering package %s", package_name
#                     )

#             cls._discovered = True

#     # -------------------------------------------------------------------------
#     # MANUAL REGISTRATION
#     # -------------------------------------------------------------------------
#     @classmethod
#     def register_executor(cls, key, executor_cls):

#         if not key or not isinstance(key, str):

#             raise ValueError("Executor key must be a valid string")

#         if not issubclass(executor_cls, ModuleExecutor):

#             raise TypeError("Executor must inherit from ModuleExecutor")

#         if key in cls._registry:

#             raise RuntimeError(f"Executor already registered for key: {key}")

#         cls._registry[key] = executor_cls

#         logger.info("[ModuleRegistry] Manually registered executor: %s", key)

#     # -------------------------------------------------------------------------
#     # EXECUTOR RETRIEVAL
#     # -------------------------------------------------------------------------
#     @classmethod
#     def get_executor(cls, key):

#         cls._discover_modules()

#         executor_cls = cls._registry.get(key)

#         if not executor_cls:
#             raise KeyError(f"No executor registered for module: {key}")


#         return executor_cls()


# # -------------------------------------------------------------------------
# # BACKWARD COMPATIBILITY EXPORTS
# # -------------------------------------------------------------------------
# registry = ModuleRegistry._registry
# register_executor = ModuleRegistry.register_executor
# get_executor = ModuleRegistry.get_executor
