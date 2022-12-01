"""smsbox.net api client module."""

import asyncio

from aiohttp import ClientSession
from aiohttp.client import ClientTimeout
from async_property import async_property

from . import exceptions


class Client:
    """API client class.

    :param aiohttp.ClientSession session: the aiohttp session to use
    :param str host: the API endpoint host, for example api.smsbox.pro (https is forced)
    :param str cleApi: the SMSBox API key, name is in French to reflect the documentation
    :param int timeout: timeout delay, default to 30 seconds
    """

    def __init__(
        self, session: ClientSession, host: str, cleApi: str, timeout: int = 30
    ):
        """Initialize the SMS."""
        self.host = host
        self.cleApi = cleApi
        self.session = session
        self.timeout = timeout

    async def __smsbox_request(self, uri: str, parameters: dict) -> str:
        """Private method to send a request to the API.

        :param str uri: the host API endpoint, for example api.php or 1.1/api.php
        :param dict parameters: parameters to pass to the API

        :returns: SMSBox API response
        :rtype: str

        :raises pysmsboxnet.exceptions.HTTPException: if HTTP status is not 200 OK
        :raises pysmsboxnet.exceptions.SMSBoxException: SMSBox API returned ERROR or timeout occurred
        :raises pysmsboxnet.exceptions.ParameterErrorException: bad parameters were passed to the API
        :raises pysmsboxnet.exceptions.AuthException: bad API key has been specified
        :raises pysmsboxnet.exceptions.BillingException: there are no enough credits to send the SMS
        :raises pysmsboxnet.exceptions.WrongRecipientException: recipient format is wrong
        :raises pysmsboxnet.exceptions.InternalErrorException: SMSBox API internal error
        """
        headers = {
            "authorization": f"App {self.cleApi}",
        }

        try:
            async with self.session.post(
                url=f"https://{self.host}/{uri}",
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

    async def send(self, dest: str, msg: str, mode: str, parameters: dict = []) -> int:
        """Send a SMS.

        :param str dest: SMS recipient(s), see API documentation about how to format
        :param str msg: the SMS message
        :param str mode: send mode,  mode API parameter
        :param dict parameters: other API parameter as strategy or if other charset than UTF8 is needed

        :returns: SMS ID if id parameter is set to 1 else 0
        :rtype: int
        """
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
        """Return float number of credits.

        :raises pysmsboxnet.exceptions.SMSBoxException: result is not OK
        """
        postData = {
            "action": "credit",
        }

        respText = await self.__smsbox_request("api.php", postData)
        if respText.startswith("CREDIT"):
            return float(respText.split(" ")[1])
        else:
            raise exceptions.SMSBoxException(respText)
