from fastapi import APIRouter, UploadFile, File

from app.services.contract_service import save_uploaded_file
from app.services.document_parser import extract_text
from app.services.contract_database import (
  create_contract_document,
  get_contract_by_id,
  save_contract_analysis,
  get_all_contracts,
  get_contract_details,
  get_contract_analysis,
  delete_contract,
)
from app.services.gemini_service import (
  generate_ai_response,
  analyze_contract,
)

router = APIRouter(
  prefix="/api/v1/contracts",
  tags=["Contracts"]
)

@router.post("/upload")
def upload_contract(file: UploadFile = File(...)): # The ... means required.
  saved_file = save_uploaded_file(file)

  extracted_text = extract_text(
    saved_file["file_path"]
  )

  contract = create_contract_document(
    filename=saved_file["filename"],
    file_type=saved_file["file_type"],
    file_path=saved_file["file_path"],
    file_size=saved_file["file_size"],
    extracted_text=extracted_text,
  )

  return {
    "message": "Contract uploaded successfully",
    "data": {
      "contract_id": contract["contract_id"],
      "filename": contract["filename"],
      "file_type": contract["file_type"],
      "file_size": contract["file_size"],
      "extracted_text": contract["extracted_text"],
    },
  }

@router.get("/test-ai")
def test_ai():
  prompt = """
  Explain in simple terms what an employment contract is.
  Keep the answer under 100 words.
  """

  response = generate_ai_response(prompt)

  return {
    "message": "Gemini connected successfully",
    "response": response,
  }

@router.get("/test-analysis")
def test_analysis():
  sample_contract = """
  EMPLOYMENT AGREEMENT

  The employee will receive salary within 60 days.
  Either party may terminate this agreement with 30 days notice.
  The employee must maintain confidentiality.
  """

  analysis = analyze_contract(sample_contract)

  return {
    "message": "Contract analysis generated successfully",
    "analysis": analysis.model_dump(),
  }

@router.post("/{contract_id}/analyze")
def analyze_existing_contract(contract_id: str):
  """
  Analyze an already uploaded contract.
  """

  # 1. Fetch contract from MongoDB
  contract = get_contract_by_id(contract_id)

  # 2. Extract previously saved text
  contract_text = contract["extracted_text"]

  # 3. Send text to Gemini
  analysis = analyze_contract(contract_text)

  # 4. Convert Pydantic model into dictionary
  analysis_data = analysis.model_dump()

  # 5. Save AI analysis in MongoDB
  save_contract_analysis(
    contract_id=contract_id,
    analysis=analysis_data,
  )

  # 6. Return response
  return {
    "message": "Contract analyzed successfully",
    "data": {
      "contract_id": contract_id,
      "filename": contract["filename"],
      "analysis": analysis_data,
    },
  }

@router.get("/")
def list_contracts():
  contracts = get_all_contracts()

  return {
    "message": "Contracts fetched successfully",
    "count": len(contracts),
    "data": contracts,
  }

@router.get("/{contract_id}")
def get_single_contract(contract_id: str):
  contract = get_contract_details(contract_id)

  return {
    "message": "Contract fetched successfully",
    "data": contract,
  }

@router.get("/{contract_id}/analysis")
def get_analysis(contract_id: str):
  analysis = get_contract_analysis(contract_id)

  return {
    "message": "Contract analysis fetched successfully",
    "data": analysis,
  }

@router.delete("/{contract_id}")
def remove_contract(contract_id: str):
  delete_contract(contract_id)

  return {
    "message": "Contract deleted successfully",
    "contract_id": contract_id,
  }