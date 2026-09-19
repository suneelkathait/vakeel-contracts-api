import json
from google import genai
import logging

from app.core.config import settings
from app.schemas.analysis import ContractAnalysis
from app.exceptions.application import AppException
from google.genai import errors

logger = logging.getLogger(__name__)

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
  logger.info(
    "Starting AI contract analysis. Text length=%s",
    len(contract_text),
  )

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

  try:
    response = client.models.generate_content(
      model="gemini-3.6-flash",
      contents=prompt,
    )

    logger.info("Gemini response received successfully")

    raw_text = response.text.strip()

    parsed_data = json.loads(raw_text)

    analysis = ContractAnalysis.model_validate(
      parsed_data
    )

    logger.info(
      "Contract analysis validated successfully",
    )

    return analysis

  except errors.APIError as e:
    logger.error(
      "Gemini API error. code=%s message=%s",
      e.code,
      e.message,
    )
    if e.code == 429:
      raise AppException(
        error_code="GEMINI_RATE_LIMIT",
        message="Gemini API rate limit exceeded. Please try again later.",
        status_code=429,
      )

    raise AppException(
      error_code="GEMINI_API_ERROR",
      message="Gemini API request failed.",
      status_code=502,
    )

  except json.JSONDecodeError:
    raise AppException(
      error_code="GEMINI_INVALID_JSON",
      message="Gemini returned an invalid JSON response.",
      status_code=422,
    )

  except Exception as e:
    logger.exception(
      "Unexpected error during contract analysis"
    )

    raise AppException(
      error_code="VALIDATION_ERROR",
      message="Gemini response does not match the expected schema.",
      status_code=422,
    )