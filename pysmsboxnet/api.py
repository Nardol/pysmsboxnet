import asyncio
from aiohttp import ClientSession
from . import exceptions

class Client:
    """API client class."""

    def __init__(self, webSession: ClientSession, host: str, cleApi: str):
        """Initialize the SMS."""
        self.host = host
        self.cleApi = cleApi
        self.session = webSession

    async def send(self, dest: str, msg: str, mode: str, parameters: dict):
        """Send a SMS."""
        headers = {"authorization": f"App {self.cleApi}",}
        postData = {
            "dest": dest,
            "msg": msg,
            "mode": mode,
            "charset": "utf-8",
        }
        postData.update(parameters)

        async with self.session.post(
            f"{self.host}/1.1/api.php", data=postData, headers=headers
        ) as resp:
            if resp.status != 200:
                raise HTTPException(resp.status)
            respText = await resp.text()
            if respText.lower() == "error":
                raise exceptions.SMSBoxException
            elif respText.lower() == "error 01":
                raise exceptions.ParameterErrorException
            elif respText.lower() == "error 02":
                raise exceptions.AuthException
            elif respText.lower() == "error 03":
                raise exceptions.BillingException
            elif respText.lower() == "error 04":
                raise exceptions.WrongRecipientException
            elif respText.lower() == "05":
                raise exceptions.InternalErrorException
