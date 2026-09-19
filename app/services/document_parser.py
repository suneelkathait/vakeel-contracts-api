from pathlib import Path
from PyPDF2 import PdfReader
from app.exceptions.application import AppException

def extract_text_from_pdf(file_path: str) -> str:
  try:
    reader = PdfReader(file_path)

    extracted_text = []

    for page in reader.pages:
      page_text = page.extract_text()

      if page_text:
        extracted_text.append(page_text)

    text = "\n".join(extracted_text).strip() # It removes unnecessary whitespace from beginning/end.

    if not text:
      raise AppException(
        error_code="TEXT_EXTRACTION_ERROR",
        status_code=400,
        detail="Could not extract text from PDF"
      )

    return text

  except Exception as error:
    raise AppException(
      error_code="TEXT_EXTRACTION_ERROR",
      message="Unable to extract text from the document",
      status_code=400,
    )


def extract_text_from_txt(file_path: str) -> str:
  try:
    text = Path(file_path).read_text(
      encoding="utf-8"
    ).strip()

    if not text:
      raise AppException(
        error_code="TEXT_EXTRACTION_ERROR",
        status_code=400,
        detail="TXT file is empty"
      )

    return text

  except Exception as error:
    raise AppException(
      error_code="TEXT_EXTRACTION_ERROR",
      message="Unable to extract text from the document",
      status_code=400,
    )


def extract_text(file_path: str) -> str:
  extension = Path(file_path).suffix.lower()

  if extension == ".pdf":
    return extract_text_from_pdf(file_path)

  if extension == ".txt":
    return extract_text_from_txt(file_path)

  raise AppException(
    error_code="VALIDATION_ERROR",
    message="Unsupported file type",
    status_code=422,
  )