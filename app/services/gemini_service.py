import json
from google import genai

from app.core.config import settings
from app.schemas.analysis import ContractAnalysis

client = genai.Client(
  api_key=settings.GEMINI_API_KEY
)

def generate_ai_response(prompt: str) -> str:
  response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
  )

  return response.text

def analyze_contract(contract_text: str) -> ContractAnalysis:
  prompt = f"""
  You are an AI assistant helping lawyers review contracts.

  Analyze the following contract.

  Return ONLY valid JSON.

  Required format:
  {{
    "overall_risk_level": "LOW",
    "key_clauses": [
      {{
        "clause_name": "string",
        "summary": "string"
      }}
    ],
    "risk_flags": [
      {{
        "risk_name": "string",
        "severity": "LOW",
        "explanation": "string"
      }}
    ],
    "recommendations": ["string"]
  }}

  Contract:
  {contract_text}
  """

  response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
  )

  raw_text = response.text.strip()

  parsed_data = json.loads(raw_text)

  return ContractAnalysis.model_validate(parsed_data)
