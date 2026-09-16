from pathlib import Path
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf", ".txt"}

def save_uploaded_file(file: UploadFile) -> dict:
  if not file.filename:
    raise HTTPException(
      status_code=400,
      detail="Filename is required"
    )

  file_extension = Path(file.filename).suffix.lower()

  if file_extension not in ALLOWED_EXTENSIONS:
    raise HTTPException(
      status_code=400,
      detail="Only PDF and TXT files are allowed"
    )

  UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

  file_path = UPLOAD_DIR / file.filename

  file_content = file.file.read()

  if not file_content:
    raise HTTPException(
      status_code=400,
      detail="Uploaded file is empty"
    )

  file_path.write_bytes(file_content)

  return {
    "filename": file.filename,
    "file_type": file_extension.replace(".", ""),
    "file_path": str(file_path),
    "file_size": len(file_content),
  }