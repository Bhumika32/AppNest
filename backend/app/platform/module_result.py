# -----------------------------------------------------------------------------
# File: backend/app/platform/module_result.py
#
# Description:
# Standardized result format returned by all AppNest module executors.
# -----------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ModuleResult:

    completed: bool = False
    score: int = 0
    status: str = "success"

    data: Dict[str, Any] = field(default_factory=dict)

    message: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:

        return {
            "completed": self.completed,
            "score": self.score,
            "status": self.status,
            "data": self.data,
            "message": self.message,
            "error": self.error
        }
# # File: backend/app/platform/module_result.py
# # -----------------------------------------------------------------------------
# # Description:
# # Standardized result format returned by all AppNest module executors.
# #
# # Benefits:
# # - Ensures consistent response structure across tools and games
# # - Enables unified XP scoring and lifecycle processing
# # - Simplifies frontend rendering logic
# # -----------------------------------------------------------------------------

# from dataclasses import dataclass, field
# from typing import Any, Dict, Optional


# @dataclass
# class ModuleResult:

#     completed: bool = False
#     score: int = 0
#     status: str = "success"

#     data: Dict[str, Any] = field(default_factory=dict)

#     message: Optional[str] = None
#     error: Optional[str] = None

#     def to_dict(self) -> Dict[str, Any]:

#         return {

#             "completed": self.completed,
#             "score": self.score,
#             "status": self.status,
#             "data": self.data,
#             "message": self.message,
#             "error": self.error
#         }
