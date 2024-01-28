"""smsbox.net api client module."""

from __future__ import annotations

import logging
from http import client as http_client

from aiohttp import ClientSession

from . import exceptions

_LOGGER = logging.getLogger(__name__)


class Client:
    """API client class.

    :param aiohttp.ClientSession session: the aiohttp session to use
    :param str host: the API endpoint host, for example api.smsbox.pro (https is forced)
    :param str cle_api: the SMSBox API key, name is in French to reflect the documentation
    """

    def __init__(self, session: ClientSession, host: str, cle_api: str):
        """Initialize the SMS."""
        self.host = host
        self.cle_api = cle_api
        self.session = session

    async def __smsbox_request(self, uri: str, parameters: dict[str, str]) -> str:
        """Private method to send a request to the API.

        :param str uri: the host API endpoint, for example api.php or 1.1/api.php
        :param dict parameters: parameters to pass to the API

        :returns: SMSBox API response
        :rtype: str

        :raises pysmsboxnet.exceptions.HTTPException: if HTTP status is not 200 OK
        :raises pysmsboxnet.exceptions.SMSBoxException: SMSBox API returned ERROR
        :raises pysmsboxnet.exceptions.ParameterErrorException: bad parameters were passed to the API
        :raises pysmsboxnet.exceptions.AuthException: bad API key has been specified
        :raises pysmsboxnet.exceptions.BillingException: there are no enough credits to send the SMS
        :raises pysmsboxnet.exceptions.WrongRecipientException: recipient format is wrong
        :raises pysmsboxnet.exceptions.InternalErrorException: SMSBox API internal error
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
        """Send a SMS.

        :param str dest: SMS recipient(s), see API documentation about how to format
        :param str msg: the SMS message
        :param str mode: send mode,  mode API parameter
        :param dict parameters: other API parameter as strategy or if other charset than UTF8 is needed

        :returns: SMS ID if id parameter is set to 1 else 0
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
        """Return float number of credits.

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
