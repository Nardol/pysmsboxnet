"""Exceptions for SMSBox API"""


class SMSBoxException(BaseException):
    """Base exception for SMSBox API."""

    def __init__(self, message="Unknown API error"):
        super().__init__(message)


class ParameterErrorException(SMSBoxException):
    """Exception when API returns ERROR 01."""

    def __init__(self):
        super().__init__("Some parameters are invalid or missing")


class AuthException(SMSBoxException):
    """Exception when API returns ERROR 02"""

    def __init__(self):
        super().__init__(
            "Unable to authenticate, check if your API key is valid or not suspended."
        )


class BillingException(SMSBoxException):
    """Exception when API returns ERROR 03."""

    def __init__(self):
        super().__init__("No enough credits, please buy some")


class WrongRecipientException(SMSBoxException):
    """Exception when API returns ERROR 04."""

    def __init__(self):
        super().__init__("Wrong recipient(s), not valid or missformated")


class InternalErrorException(SMSBoxException):
    """Exception when API returns ERROR 05."""

    def __init__(self):
        super().__init__("SMSBox.net internal error, try again later")


class HTTPException(SMSBoxException):
    """Exception when API returns ERROR 03."""

    def __init__(self, errorCode):
        super().__init__(f"HTTP error ({errorCode})")
