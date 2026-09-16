from datetime import datetime, timezone
from bson import ObjectId
import logging
from app.database.mongodb import contracts_collection
from app.exceptions.application import AppException

logger = logging.getLogger(__name__)

def create_contract_document(
  filename: str,
  file_type: str,
  file_path: str,
  file_size: int,
  extracted_text: str,
):
  contract_document = {
    "filename": filename,
    "file_type": file_type,
    "file_path": file_path,
    "file_size": file_size,
    "extracted_text": extracted_text,
    "analysis": None,
    "created_at": datetime.now(timezone.utc),
  }

  result = contracts_collection.insert_one(contract_document)

  return {
    "contract_id": str(result.inserted_id),
    **contract_document,
  }

def get_contract_by_id(contract_id: str):
  """
  Fetch a contract document from MongoDB using its ID.
  """

  if not ObjectId.is_valid(contract_id):
    raise AppException(
      message="Invalid contract ID provided",
      status_code=400,
    )

  contract = contracts_collection.find_one(
    {"_id": ObjectId(contract_id)}
  )

  if not contract:
    raise AppException(
      message="Contract not found",
      status_code=400,
    )

  return contract


def save_contract_analysis(
  contract_id: str,
  analysis: dict,
):
  """
  Save AI analysis into the existing contract document.
  """
  logger.info(
    "Saving contract analysis: contract_id=%s",
    contract_id,
  )

  if not ObjectId.is_valid(contract_id):
    raise AppException(
      message="Invalid contract ID provided",
      status_code=400,
    )

  result = contracts_collection.update_one(
    {"_id": ObjectId(contract_id)},
    {
      "$set": {
        "analysis": analysis,
        "analyzed_at": datetime.now(timezone.utc),
      }
    },
  )

  if result.matched_count == 0:
    raise AppException(
      message="Contract not found",
      status_code=400,
    )

  return True

def get_all_contracts():
  """
  Fetch all contracts from MongoDB.
  """

  contracts = contracts_collection.find().sort(
    "created_at",
    -1,
  )

  contract_list = []

  for contract in contracts:
    contract_list.append({
      "contract_id": str(contract["_id"]),
      "filename": contract["filename"],
      "file_type": contract["file_type"],
      "file_size": contract["file_size"],
      "created_at": contract["created_at"],
      "has_analysis": contract.get("analysis") is not None,
    })

  return contract_list

def get_contract_details(contract_id: str):
  """
  Fetch complete contract details by ID.
  """

  if not ObjectId.is_valid(contract_id):
    raise AppException(
      message="Invalid contract ID provided",
      status_code=400,
    )

  contract = contracts_collection.find_one(
    {"_id": ObjectId(contract_id)}
  )

  if not contract:
    raise AppException(
      message="Contract not found",
      status_code=400,
    )

  return {
    "contract_id": str(contract["_id"]),
    "filename": contract["filename"],
    "file_type": contract["file_type"],
    "file_path": contract["file_path"],
    "file_size": contract["file_size"],
    "extracted_text": contract.get("extracted_text"),
    "analysis": contract.get("analysis"),
    "created_at": contract.get("created_at"),
    "analyzed_at": contract.get("analyzed_at"),
  }

def get_contract_analysis(contract_id: str):
  """
  Fetch only the AI analysis of a contract.
  """

  if not ObjectId.is_valid(contract_id):
    raise AppException(
      message="Invalid contract ID provided",
      status_code=400,
    )

  contract = contracts_collection.find_one(
    {"_id": ObjectId(contract_id)},
    {
      "filename": 1,
      "analysis": 1,
      "analyzed_at": 1,
    },
  )

  if not contract:
    raise AppException(
      message="Contract not found",
      status_code=400,
    )

  return {
    "contract_id": str(contract["_id"]),
    "filename": contract["filename"],
    "analysis": contract.get("analysis"),
    "analyzed_at": contract.get("analyzed_at"),
  }

def delete_contract(contract_id: str):
  """
  Delete a contract from MongoDB.
  """

  if not ObjectId.is_valid(contract_id):
    raise AppException(
      message="Invalid contract ID provided",
      status_code=400,
    )

  result = contracts_collection.delete_one(
    {"_id": ObjectId(contract_id)}
  )

  if result.deleted_count == 0:
    raise AppException(
      message="Contract not found",
      status_code=400,
    )

  return True

def update_contract_metadata(
  contract_id: str,
  update_data: dict,
):
  """
  Update editable contract metadata.
  """

  if not ObjectId.is_valid(contract_id):
    raise AppException(
      message="Invalid contract ID provided",
      status_code=400,
    )

  update_fields = {
    key: value
    for key, value in update_data.items()
    if value is not None
  }

  if not update_fields:
    raise AppException(
      message="At least one field is required for update",
      status_code=422,
    )

  result = contracts_collection.update_one(
    {"_id": ObjectId(contract_id)},
    {
      "$set": update_fields,
    },
  )

  if result.matched_count == 0:
    raise AppException(
      message="Contract not found",
      status_code=400,
    )

  return get_contract_details(contract_id)