from pathlib import Path
import logging
from fastapi import UploadFile
from app.exceptions.application import AppException

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf", ".txt"}

def save_uploaded_file(file: UploadFile) -> dict:
  if not file.filename:
    raise AppException(
      error_code="VALIDATION_ERROR",
      message="Filename is required",
      status_code=422,
    )

  logger.info(
    "Uploading contract: filename=%s",
    file.filename,
  )

  file_extension = Path(file.filename).suffix.lower()

  if file_extension not in ALLOWED_EXTENSIONS:
    logger.warning(
      "Rejected file type: filename=%s, extension=%s",
      file.filename,
      file_extension,
    )

    raise AppException(
      error_code="INVALID_FILE_TYPE",
      message="Only PDF and TXT files are allowed",
      status_code=400,
    )

  UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  file_path = UPLOAD_DIR / file.filename

  file_content = file.file.read()

  if not file_content:
    logger.warning(
      "Empty file uploaded: filename=%s",
      file.filename,
    )

    raise AppException(
      error_code="EMPTY_FILE",
      message="Uploaded file is empty",
      status_code=400,
    )

  file_path.write_bytes(file_content)

  logger.info(
    "Contract uploaded successfully: filename=%s, size=%s",
    file.filename,
    len(file_content),
  )

  return {
    "filename": file.filename,
    "file_type": file_extension.replace(".", ""),
    "file_path": str(file_path),
    "file_size": len(file_content),
  }