from pydantic import BaseModel
from typing import List, Literal

class KeyClause(BaseModel):
  clause_name: str
  summary: str

class RiskFlag(BaseModel):
  risk_name: str
  severity: Literal["LOW", "MEDIUM", "HIGH"]
  explanation: str

class ContractAnalysis(BaseModel):
  overall_risk_level: Literal["LOW", "MEDIUM", "HIGH"]
  key_clauses: List[KeyClause]
  risk_flags: List[RiskFlag]
  recommendations: List[str]