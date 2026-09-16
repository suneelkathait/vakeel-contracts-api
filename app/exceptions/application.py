class AppException(Exception):
  """
  Base application exception.
  """

  def __init__(
    self,
    message: str,
    status_code: int = 400,
  ):
    self.message = message
    self.status_code = status_code

    super().__init__(message)

class ContractNotFoundException(AppException):
  def __init__(self):
    super().__init__(
      message="Contract not found",
      status_code=404,
    )

class InvalidFileTypeException(AppException):
  def __init__(self):
    super().__init__(
      message="Only PDF and TXT files are allowed",
      status_code=400,
    )

class EmptyFileException(AppException):
  def __init__(self):
    super().__init__(
      message="Uploaded file is empty",
      status_code=400,
    )

class TextExtractionException(AppException):
  def __init__(self):
    super().__init__(
      message="Unable to extract text from the document",
      status_code=400,
    )

class AIAnalysisException(AppException):
  def __init__(self):
    super().__init__(
      message="Unable to analyze the contract using AI",
      status_code=500,
    )

class InvalidContractIDException(AppException):
  def __init__(self):
    super().__init__(
      message="Invalid contract ID provided",
      status_code=400,
    )