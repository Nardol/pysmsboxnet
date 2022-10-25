import asyncio
from aiohttp import ClientSession
from aiohttp.client import ClientTimeout
from . import exceptions


class Client:
    """API client class."""

    def __init__(
        self, webSession: ClientSession, host: str, cleApi: str, defaultTimeout=30
    ):
        """Initialize the SMS."""
        self.host = host
        self.cleApi = cleApi
        self.session = webSession
        self.timeout = defaultTimeout

    async def send(self, dest: str, msg: str, mode: str, parameters: dict):
        """Send a SMS."""
        headers = {
            "authorization": f"App {self.cleApi}",
        }
        postData = {
            "dest": dest,
            "msg": msg,
            "mode": mode,
            "charset": "utf-8",
        }
        postData.update(parameters)

        try:
            async with self.session.post(
                url=f"{self.host}/1.1/api.php",
                headers=headers,
                data=postData,
                timeout=ClientTimeout(total=self.timeout),
            ) as resp:
                if resp.status != 200:
                    raise exceptions.HTTPException(resp.status)
                respText = await resp.text()
                if respText == "ERROR":
                    raise exceptions.SMSBoxException
                elif respText == "ERROR 01":
                    raise exceptions.ParameterErrorException
                elif respText == "ERROR 02":
                    raise exceptions.AuthException
                elif respText == "ERROR 03":
                    raise exceptions.BillingException
                elif respText == "ERROR 04":
                    raise exceptions.WrongRecipientException
                elif respText == "ERROR 05":
                    raise exceptions.InternalErrorException
        except asyncio.TimeoutError as exception:
            raise exceptions.SMSBoxException(
                f"Timeout of {self.timeout} seconds was "
                f"reached while sending the SMS"
            ) from exception
