"""SMSBox API client module."""

from __future__ import annotations

import asyncio
import logging
import re
from collections.abc import Mapping
from http import client as http_client

from aiohttp import ClientError, ClientSession, ClientTimeout
from aiohttp import __version__ as aiohttp_version
from yarl import URL

from . import __version__ as pkg_version
from . import exceptions

_LOGGER = logging.getLogger(__name__)


class Client:
    """API client class.

    :param aiohttp.ClientSession session: the aiohttp session to use
    :param str host: the API endpoint host, for example ``api.smsbox.pro`` (HTTPS is enforced)
    :param str cle_api: the SMSBox API key; the parameter name is in French to match the official documentation
    :param timeout: request timeout (seconds or ``aiohttp.ClientTimeout``), default 10s
    :param headers: optional extra headers (can override ``User-Agent`` if provided)
    """

    def __init__(
        self,
        session: ClientSession,
        host: str,
        cle_api: str,
        *,
        timeout: ClientTimeout | float | None = None,
        headers: Mapping[str, str] | None = None,
    ):
        """Initialize the client."""
        # Basic validation of host to avoid accidental schema/paths
        if not host or "/" in host or "://" in host or " " in host:
            raise ValueError("host must be a bare hostname, e.g. 'api.smsbox.pro'")

        # Support optional port in host (e.g. "localhost:8443" or "[::1]:8443").
        try:
            parsed_host = URL("https://" + host)
        except ValueError as err:  # pragma: no cover - defensive
            raise ValueError("invalid host format") from err

        self.host = parsed_host.host or host
        self._port = parsed_host.port
        self.cle_api = cle_api
        self.session = session

        if timeout is None:
            self._timeout = ClientTimeout(total=10)
        elif isinstance(timeout, (int, float)):  # noqa: UP038
            self._timeout = ClientTimeout(total=float(timeout))
        else:
            self._timeout = timeout

        self._user_agent = f"pysmsboxnet/{pkg_version} aiohttp/{aiohttp_version}"
        self._headers_extra = dict(headers or {})

    @staticmethod
    def _redact(parameters: Mapping[str, str]) -> dict[str, str]:
        """Return a redacted copy of parameters for safe logging."""
        redacted = dict(parameters)
        for key in ("msg", "dest"):
            if key in redacted:
                redacted[key] = "<redacted>"
        return redacted

    async def _smsbox_request(self, uri: str, parameters: Mapping[str, str]) -> str:
        """Send a request to the API (internal helper).

        :param str uri: the API path, for example ``api.php`` or ``1.1/api.php``
        :param Mapping parameters: form parameters to pass to the API

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
            "User-Agent": self._headers_extra.get("User-Agent", self._user_agent),
        }
        if self._headers_extra:
            headers.update(self._headers_extra)

        _LOGGER.debug(
            "Sending request to SMSBox API using host %s with URI %s and parameters %s",
            self.host,
            uri,
            self._redact(parameters),
        )
        url = URL.build(
            scheme="https",
            host=self.host,
            port=self._port,
            path=f"/{uri.lstrip('/')}",
        )
        try:
            async with self.session.post(
                url=url.human_repr(),
                headers=headers,
                data=parameters,
                timeout=self._timeout,
            ) as resp:
                _LOGGER.debug("HTTP response: %s", resp.status)
                if resp.status != http_client.OK:
                    raise exceptions.HTTPException(resp.status)
                resp_text = (await resp.text()).strip()
                _LOGGER.debug("API response: %s", resp_text)

                error_map: dict[str, type[exceptions.SMSBoxException]] = {
                    "ERROR": exceptions.SMSBoxException,
                    "ERROR 01": exceptions.ParameterErrorException,
                    "ERROR 02": exceptions.AuthException,
                    "ERROR 03": exceptions.BillingException,
                    "ERROR 04": exceptions.WrongRecipientException,
                    "ERROR 05": exceptions.InternalErrorException,
                }
                if resp_text in error_map:
                    raise error_map[resp_text]()

                return resp_text
        except (TimeoutError, Exception) as err:
            # Re-map aiohttp network exceptions to a library-specific one
            # while preserving HTTPException raised above.
            if isinstance(err, exceptions.SMSBoxException):
                raise
            if isinstance(err, (ClientError, asyncio.TimeoutError)):  # noqa: UP038
                raise exceptions.NetworkException(str(err)) from err
            raise

    async def send(
        self,
        dest: str,
        msg: str,
        mode: str,
        parameters: Mapping[str, str] | None = None,
    ) -> int:
        """Send an SMS.

        :param str dest: SMS recipient(s); see the API documentation for the required format
        :param str msg: the SMS message
        :param str mode: send mode (the ``mode`` API parameter)
        :param dict parameters: optional API parameters (e.g., ``strategy``), or a charset other than UTF-8

        :returns: SMS ID if the ``id`` parameter is set to ``1``; otherwise ``0``
        :rtype: int
        """
        post_data: dict[str, str] = {
            "dest": dest,
            "msg": msg,
            "mode": mode,
            "charset": "utf-8",
        }
        if parameters:
            post_data.update(dict(parameters))

        resp_text = await self._smsbox_request("1.1/api.php", post_data)
        m = re.match(r"^OK(?:\s+(\d+))?$", resp_text)
        if not m:
            raise exceptions.SMSBoxException(resp_text)
        return int(m.group(1)) if m.group(1) else 0

    async def get_credits(self) -> float:
        """Return the number of credits as a float.

        :raises pysmsboxnet.exceptions.SMSBoxException: result is not OK
        """
        post_data = {
            "action": "credit",
        }

        resp_text = await self._smsbox_request("api.php", post_data)
        m = re.match(r"^CREDIT\s+([0-9]+(?:\.[0-9]+)?)$", resp_text)
        if m:
            return float(m.group(1))
        raise exceptions.SMSBoxException(resp_text)
