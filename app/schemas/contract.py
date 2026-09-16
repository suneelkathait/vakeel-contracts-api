from typing import Optional
from pydantic import BaseModel, Field

class ContractUpdateRequest(BaseModel):
  filename: Optional[str] = Field(
    default=None,
    min_length=1,
    max_length=255,
  )

  description: Optional[str] = Field(
    default=None,
    max_length=1000,
  )