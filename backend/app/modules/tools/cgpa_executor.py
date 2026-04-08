from app.platform.module_executor import ModuleExecutor
from app.platform.module_result import ModuleResult

class CGPAExecutor(ModuleExecutor):
    module_key = "CGPACalculator"
    
    def execute(self, payload: dict, user) -> ModuleResult:
        metadata = payload.get("metadata", {})
        grades = payload.get("grades") or metadata.get("grades", [])
        
        if not grades:
            return ModuleResult(
                completed=False,
                status="error",
                error="INVALID_INPUT",
                message="No grades provided"
            )
            
        try:
            cgpa = sum(float(g) for g in grades) / len(grades)
            return ModuleResult(
                completed=True,
                status="success",
                data={"cgpa": round(cgpa, 2)}
            )
        except Exception as e:
            return ModuleResult(
                completed=False,
                status="error",
                error="CALCULATION_ERROR",
                message=str(e)
            )