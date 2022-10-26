"""Exceptions for SMSBox API."""


class SMSBoxException(BaseException):
    """Base exception for SMSBox API."""

    def __init__(self, message="Unknown API error"):
        """Initialize SMSBox base exception.

        An optional message can be specified.
        """
        super().__init__(message)


class ParameterErrorException(SMSBoxException):
    """Exception when API returns ERROR 01."""

    def __init__(self):
        """Initialize for bad parameters exception."""
        super().__init__("Some parameters are invalid or missing")


class AuthException(SMSBoxException):
    """Exception when API returns ERROR 02."""

    def __init__(self):
        """Initialize authorization error, no message to specify."""
        super().__init__(
            "Unable to authenticate,"
            " check if your API key is valid or not suspended."
        )


class BillingException(SMSBoxException):
    """xception when API returns ERROR 03."""

    def __init__(self):
        """Initialize when no enough SMS credits, no message to specify."""
        super().__init__("No enough credits, please buy some")


class WrongRecipientException(SMSBoxException):
    """Exception when API returns ERROR 04."""

    def __init__(self):
        """Initialize when recipient is bad, no message to specify."""
        super().__init__("Wrong recipient(s), not valid or missformated")


class InternalErrorException(SMSBoxException):
    """Exception when API returns ERROR 05."""

    def __init__(self):
        """Initialize internal error."""
        super().__init__("SMSBox.net internal error, try again later")


class HTTPException(SMSBoxException):
    """Exception when API returns ERROR 03."""

    def __init__(self, errorCode):
        """Initialize HTTP error Exception."""
        super().__init__(f"HTTP error ({errorCode})")
