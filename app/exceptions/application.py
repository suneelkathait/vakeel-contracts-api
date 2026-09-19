class AppException(Exception):
  """
  Base application exception.
  """

  def __init__(
    self,
    message: str,
    status_code: int = 400,
    error_code: str = "APPLICATION_ERROR",
  ):
    self.message = message
    self.status_code = status_code
    self.error_code = error_code

    super().__init__(message)

# class InvalidFileTypeException(AppException):
#   def __init__(self):
#     super().__init__(
#       error_code="INVALID_FILE_TYPE",
#       message="Only PDF and TXT files are allowed",
#       status_code=400,
#     )