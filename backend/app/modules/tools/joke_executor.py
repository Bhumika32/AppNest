from app.platform.module_executor import ModuleExecutor
from app.platform.module_result import ModuleResult
import random

class JokeExecutor(ModuleExecutor):
    module_key = "JokeGenerator"
    
    def execute(self, payload: dict, user) -> ModuleResult:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "I would tell you a UDP joke, but you might not get it.",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Why did the database administrator leave his wife? She had one-to-many relationships.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem."
        ]
        return ModuleResult(
            completed=True,
            status="success",
            data={"joke": random.choice(jokes)}
        )
