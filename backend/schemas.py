from pydantic import BaseModel
from typing import List


class IssueAnalysis(BaseModel):
    summary: str
    type: str
    priority_score: str
    suggested_labels: List[str]
    potential_impact: str
