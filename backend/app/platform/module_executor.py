# -----------------------------------------------------------------------------
# File: backend/app/platform/module_executor.py
#
# Description:
# Base class for all AppNest module executors.
#
# Responsibilities:
# - Define execution interface for tools and games
# - Provide safe execution wrapper
# - Convert ModuleResult objects to dictionary format
#
# Rules for Executors:
# - Must only contain module logic
# - Must NOT handle:
#     * XP
#     * notifications
#     * analytics
#     * database writes unrelated to module output
# -----------------------------------------------------------------------------

import logging
from app.platform.module_result import ModuleResult

logger = logging.getLogger(__name__)


class ModuleExecutor:

    module_key = None

    def execute(self, payload: dict, user) -> ModuleResult:
        """
        Execute module logic.
        Must return a ModuleResult object.
        """
        raise NotImplementedError

    def safe_execute(self, payload: dict, user) -> dict:
        """
        Execute module safely and return normalized dictionary result.
        """

        try:

            result = self.execute(payload, user)

            if isinstance(result, ModuleResult):
                return result.to_dict()

            return result

        except Exception as e:

            logger.exception("Module execution failed")

            return ModuleResult(
                completed=False,
                status="error",
                error="MODULE_EXECUTION_FAILED",
                message=str(e)
            ).to_dict()
# # File: backend/app/platform/module_executor.py
# # -----------------------------------------------------------------------------
# # Description:
# # Base class for all AppNest module executors.
# #
# # Responsibilities:
# # - Define execution interface for tools and games
# # - Provide safe execution wrapper
# # - Convert ModuleResult objects to dictionary format
# #
# # Rules for Executors:
# # - Must only contain module logic
# # - Must NOT handle:
# #     * XP
# #     * notifications
# #     * analytics
# #     * database writes unrelated to module output
# # -----------------------------------------------------------------------------

# from app.platform.module_result import ModuleResult


# class ModuleExecutor:

#     module_key = None

#     def execute(self, payload: dict, user) -> ModuleResult:
#         """
#         Execute module logic.

#         Must return a ModuleResult object.
#         """
#         raise NotImplementedError

#     def safe_execute(self, payload: dict, user) -> dict:
#         """
#         Execute module safely and return normalized dictionary result.
#         """

#         try:

#             result = self.execute(payload, user)

#             if isinstance(result, ModuleResult):

#                 return result.to_dict()

#             return result

#         except Exception as e:

#             import traceback
#             traceback.print_exc()

#             return ModuleResult(
#                 completed=False,
#                 status="error",
#                 error="MODULE_EXECUTION_FAILED",
#                 message=str(e)
#             ).to_dict()
# # from app.platform.module_result import ModuleResult

# # class ModuleExecutor:
# #     module_key = None

# #     def execute(self, payload: dict, user) -> ModuleResult:
# #         """
# #         Executes module logic only.
# #         Returns a ModuleResult object.
# #         Must NOT handle:
# #         - XP
# #         - analytics
# #         - notifications
# #         - database commits unrelated to module result
# #         """
# #         raise NotImplementedError

# #     def safe_execute(self, payload: dict, user) -> dict:
# #         """
# #         Executes module safely and returns a dictionary matching ModuleResult structure.
# #         """
# #         try:
# #             result = self.execute(payload, user)
# #             if isinstance(result, ModuleResult):
# #                 return result.to_dict()
# #             return result
# #         except Exception as e:
# #             import traceback
# #             traceback.print_exc()
# #             return ModuleResult(
# #                 completed=False,
# #                 status="error",
# #                 error="MODULE_EXECUTION_FAILED",
# #                 message=str(e)
# #             ).to_dict()
