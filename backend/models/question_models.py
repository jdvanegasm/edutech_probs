from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class ProblemRequest(BaseModel):
    id: str
    mode: str
    params_override: Optional[Dict[str, Any]] = None

class GeneratedProblem(BaseModel):
    id: str
    statement: str
    params: Dict[str, Any]
    correct_answer: Optional[Any] = None

class TestRequest(BaseModel):
    num_questions: int = 5

class TestQuestion(BaseModel):
    id: str
    statement: str
    options: List[float]

class GradeItem(BaseModel):
    id: str
    selected: float
    correct: float

class GradeRequest(BaseModel):
    answers: List[GradeItem]

class GradeResponse(BaseModel):
    score: float
    details: List[Dict[str, Any]]