"""SMSBox API client module."""

from __future__ import annotations

import logging
from http import client as http_client

from aiohttp import ClientSession

from . import exceptions

_LOGGER = logging.getLogger(__name__)


class Client:
    """API client class.

    :param aiohttp.ClientSession session: the aiohttp session to use
    :param str host: the API endpoint host, for example ``api.smsbox.pro`` (HTTPS is enforced)
    :param str cle_api: the SMSBox API key; the parameter name is in French to match the official documentation
    """

    def __init__(self, session: ClientSession, host: str, cle_api: str):
        """Initialize the client."""
        self.host = host
        self.cle_api = cle_api
        self.session = session

    async def __smsbox_request(self, uri: str, parameters: dict[str, str]) -> str:
        """Send a request to the API (internal helper).

        :param str uri: the API path, for example ``api.php`` or ``1.1/api.php``
        :param dict parameters: form parameters to pass to the API

        :returns: SMSBox API response
        :rtype: str

        :raises pysmsboxnet.exceptions.HTTPException: HTTP status is not 200 OK
        :raises pysmsboxnet.exceptions.SMSBoxException: API returned ``ERROR``
        :raises pysmsboxnet.exceptions.ParameterErrorException: invalid or missing parameters
        :raises pysmsboxnet.exceptions.AuthException: bad API key specified
        :raises pysmsboxnet.exceptions.BillingException: not enough credits to send the SMS
        :raises pysmsboxnet.exceptions.WrongRecipientException: recipient format is wrong
        :raises pysmsboxnet.exceptions.InternalErrorException: API internal error
        """
        headers = {
            "authorization": f"App {self.cle_api}",
        }

        _LOGGER.debug(
            "Sending request to SMSBox API using host %s with URI %s and parameters %s",
            self.host,
            uri,
            parameters,
        )
        async with self.session.post(
            url=f"https://{self.host}/{uri}",
            headers=headers,
            data=parameters,
        ) as resp:
            _LOGGER.debug("HTTP response: %s", resp.status)
            if resp.status != http_client.OK:
                raise exceptions.HTTPException(resp.status)
            resp_text = await resp.text()
            _LOGGER.debug("API response: %s", resp_text)
            if resp_text == "ERROR":
                raise exceptions.SMSBoxException
            elif resp_text == "ERROR 01":
                raise exceptions.ParameterErrorException
            elif resp_text == "ERROR 02":
                raise exceptions.AuthException
            elif resp_text == "ERROR 03":
                raise exceptions.BillingException
            elif resp_text == "ERROR 04":
                raise exceptions.WrongRecipientException
            elif resp_text == "ERROR 05":
                raise exceptions.InternalErrorException
            else:
                return resp_text

    async def send(
        self, dest: str, msg: str, mode: str, parameters: dict[str, str] | None = None
    ) -> int:
        """Send an SMS.

        :param str dest: SMS recipient(s); see the API documentation for the required format
        :param str msg: the SMS message
        :param str mode: send mode (the ``mode`` API parameter)
        :param dict parameters: optional API parameters (e.g., ``strategy``), or a charset other than UTF-8

        :returns: SMS ID if the ``id`` parameter is set to ``1``; otherwise ``0``
        :rtype: int
        """
        post_data = {
            "dest": dest,
            "msg": msg,
            "mode": mode,
            "charset": "utf-8",
        }
        if parameters:
            post_data.update(parameters)

        resp_text = await self.__smsbox_request("1.1/api.php", post_data)

        resp_ok = resp_text.split(" ")
        if len(resp_ok) == 1:
            return 0
        return int(resp_ok[1])

    async def get_credits(self) -> float:
        """Return the number of credits as a float.

        :raises pysmsboxnet.exceptions.SMSBoxException: result is not OK
        """
        post_data = {
            "action": "credit",
        }

        resp_text = await self.__smsbox_request("api.php", post_data)
        if resp_text.startswith("CREDIT"):
            return float(resp_text.split(" ")[1])
        else:
            raise exceptions.SMSBoxException(resp_text)
