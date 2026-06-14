from pydantic import BaseModel
from typing import Optional


class RunRequest(BaseModel):
    task: str
    max_iterations: Optional[int] = 10


class RunResponse(BaseModel):
    result: str
    iterations: int
    tool_calls_made: list[str]
