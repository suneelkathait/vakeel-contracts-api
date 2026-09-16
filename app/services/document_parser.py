from pathlib import Path
from PyPDF2 import PdfReader
from fastapi import HTTPException

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
      raise HTTPException(
        status_code=400,
        detail="Could not extract text from PDF"
      )

    return text

  except HTTPException:
      raise

  except Exception as error:
    raise HTTPException(
      status_code=400,
      detail=f"Failed to read PDF: {str(error)}"
    )


def extract_text_from_txt(file_path: str) -> str:
  try:
    text = Path(file_path).read_text(
      encoding="utf-8"
    ).strip()

    if not text:
      raise HTTPException(
        status_code=400,
        detail="TXT file is empty"
      )

    return text

  except HTTPException:
    raise

  except Exception as error:
    raise HTTPException(
      status_code=400,
      detail=f"Failed to read TXT file: {str(error)}"
    )


def extract_text(file_path: str) -> str:
  extension = Path(file_path).suffix.lower()

  if extension == ".pdf":
    return extract_text_from_pdf(file_path)

  if extension == ".txt":
    return extract_text_from_txt(file_path)

  raise HTTPException(
    status_code=400,
    detail="Unsupported file type"
  )