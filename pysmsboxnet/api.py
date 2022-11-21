"""smsbox.net api client module."""

import asyncio

from aiohttp import ClientSession
from aiohttp.client import ClientTimeout
from async_property import async_property

from . import exceptions


class Client:
    """API client class."""

    def __init__(self, session: ClientSession, host: str, cleApi: str, timeout=30):
        """Initialize the SMS."""
        self.host = host
        self.cleApi = cleApi
        self.session = session
        self.timeout = timeout

    async def __smsbox_request(self, uri: str, parameters: dict) -> str:
        """Send a request to the API."""
        headers = {
            "authorization": f"App {self.cleApi}",
        }

        try:
            async with self.session.post(
                url=f"{self.host}/{uri}",
                headers=headers,
                data=parameters,
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
                else:
                    return respText
        except asyncio.TimeoutError as exception:
            raise exceptions.SMSBoxException(
                f"Timeout of {self.timeout} seconds was "
                f"reached while sending the SMS"
            ) from exception

    async def send(self, dest: str, msg: str, mode: str, parameters: dict) -> int:
        """Send a SMS."""
        postData = {
            "dest": dest,
            "msg": msg,
            "mode": mode,
            "charset": "utf-8",
        }
        postData.update(parameters)

        respText = await self.__smsbox_request("1.1/api.php", postData)

        if respText.startswith("OK"):
            respOK = respText.split(" ")
            if len(respOK) == 1:
                return 0
            return int(respOK[1])

    @async_property
    async def credits(self) -> float:
        """Return number of credits."""
        postData = {
            "action": "credit",
        }

        respText = await self.__smsbox_request("api.php", postData)
        if respText.startswith("CREDIT"):
            return float(respText.split(" ")[1])
        else:
            raise exceptions.SMSBoxException(respText)
