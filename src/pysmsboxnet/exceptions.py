"""Exceptions for SMSBox API."""


class SMSBoxException(Exception):  # noqa: N818
    """Base exception for SMSBox API."""

    def __init__(self, message: str = "Unknown API error"):
        """Initialize SMSBox base exception.

        An optional message can be specified.
        """
        super().__init__(message)


class ParameterErrorException(SMSBoxException):
    """Exception raised when the API returns ERROR 01."""

    def __init__(self) -> None:
        """Initialize for bad parameters exception."""
        super().__init__("Some parameters are invalid or missing")


class AuthException(SMSBoxException):
    """Exception raised when the API returns ERROR 02."""

    def __init__(self) -> None:
        """Initialize authorization error, no message to specify."""
        super().__init__(
            "Unable to authenticate. Check that your API key is valid and not suspended."
        )


class BillingException(SMSBoxException):
    """Exception raised when the API returns ERROR 03."""

    def __init__(self) -> None:
        """Initialize when no enough SMS credits, no message to specify."""
        super().__init__("Not enough credits; please buy more")


class WrongRecipientException(SMSBoxException):
    """Exception raised when the API returns ERROR 04."""

    def __init__(self) -> None:
        """Initialize when recipient is bad, no message to specify."""
        super().__init__("Invalid recipient(s): not valid or misformatted")


class InternalErrorException(SMSBoxException):
    """Exception raised when the API returns ERROR 05."""

    def __init__(self) -> None:
        """Initialize internal error."""
        super().__init__("SMSBox internal error; try again later")


class HTTPException(SMSBoxException):
    """Exception raised when the HTTP status is not successful."""

    def __init__(self, error_code: int):
        """Initialize HTTP error Exception."""
        super().__init__(f"HTTP error ({error_code})")
