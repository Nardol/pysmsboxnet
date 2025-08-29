"""Tests for pysmsboxnet."""

from __future__ import annotations

import logging
import random
from typing import Any

import aiohttp
import pytest

from pysmsboxnet import exceptions
from pysmsboxnet.api import Client

# Sessions rely on the async context manager for cleanup.

# Constants
SMSBOX_HOST = "api.smsbox.pro"
SMSBOX_API_KEY = "pub-xxxxx-xxxxx-xxxx-xxxx-xxxxx-xxxxxxxx"
SMS_RECIPIENT = "9999001"
SMS_MSG = "Test d'un message ! En plus il va être envoyé."
SEND_MODE = "expert"
SMSBOX_STRATEGY = "2"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("api_text", "exc"),
    [
        ("ERROR 01", exceptions.ParameterErrorException),
        ("ERROR 02", exceptions.AuthException),
        ("ERROR 03", exceptions.BillingException),
        ("ERROR 04", exceptions.WrongRecipientException),
        ("ERROR 05", exceptions.InternalErrorException),
        ("ERROR", exceptions.SMSBoxException),
    ],
)
async def test_send_errors_param(
    aresponses: Any, api_text: str, exc: type[Exception]
) -> None:
    """Test mapping of error responses to exceptions (parametrized)."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(text=api_text, status=200),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(session, SMSBOX_HOST, SMSBOX_API_KEY)
        with pytest.raises(exc):
            await sms.send(
                SMS_RECIPIENT,
                SMS_MSG,
                SEND_MODE,
                {"strategy": SMSBOX_STRATEGY},
            )


# Old individual error tests are superseded by the parametrized test above.


@pytest.mark.asyncio
async def test_send_unknown_response_raises(aresponses: Any) -> None:
    """Test that an unexpected send response raises an exception."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(text="FFF", status=200),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(session, SMSBOX_HOST, SMSBOX_API_KEY)
        with pytest.raises(exceptions.SMSBoxException):
            await sms.send(
                SMS_RECIPIENT, SMS_MSG, SEND_MODE, {"strategy": SMSBOX_STRATEGY}
            )


@pytest.mark.asyncio
async def test_network_timeout_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that a timeout is mapped to NetworkException."""
    async with aiohttp.ClientSession() as session:
        sms = Client(session, SMSBOX_HOST, SMSBOX_API_KEY, timeout=0.1)

        def raise_timeout(*_a: Any, **_k: Any) -> Any:
            raise TimeoutError()

        monkeypatch.setattr(session, "post", raise_timeout)

        with pytest.raises(exceptions.NetworkException):
            await sms.send(
                SMS_RECIPIENT, SMS_MSG, SEND_MODE, {"strategy": SMSBOX_STRATEGY}
            )


@pytest.mark.asyncio
async def test_network_client_error_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that a ClientError is mapped to NetworkException."""
    async with aiohttp.ClientSession() as session:
        sms = Client(session, SMSBOX_HOST, SMSBOX_API_KEY)

        def raise_client_error(*_a: Any, **_k: Any) -> Any:
            raise aiohttp.ClientError("boom")

        monkeypatch.setattr(session, "post", raise_client_error)

        with pytest.raises(exceptions.NetworkException):
            await sms.send(
                SMS_RECIPIENT, SMS_MSG, SEND_MODE, {"strategy": SMSBOX_STRATEGY}
            )


@pytest.mark.asyncio
async def test_logs_redact_msg_and_dest(
    aresponses: Any, caplog: pytest.LogCaptureFixture
) -> None:
    """Ensure logs do not expose sensitive fields."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(text="OK 123", status=200),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(session, SMSBOX_HOST, SMSBOX_API_KEY)
        caplog.set_level(logging.DEBUG, logger="pysmsboxnet.api")
        dest_val = "+33123456789"
        msg_val = "hello secret"
        await sms.send(
            dest_val, msg_val, SEND_MODE, {"strategy": SMSBOX_STRATEGY, "id": "1"}
        )
        text = caplog.text
        assert dest_val not in text
        assert msg_val not in text
        assert "<redacted>" in text


@pytest.mark.asyncio
async def test_http_error(aresponses: Any) -> None:
    """Test if HTTP status is not 200."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(
            text="",
            status=500,
        ),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(
            session,
            SMSBOX_HOST,
            SMSBOX_API_KEY,
        )
        with pytest.raises(exceptions.HTTPException):
            await sms.send(
                SMS_RECIPIENT,
                SMS_MSG,
                SEND_MODE,
                {"strategy": SMSBOX_STRATEGY},
            )


@pytest.mark.asyncio
async def test_ok(aresponses: Any) -> None:
    """Test result OK without ID."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(
            text="OK",
            status=200,
        ),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(
            session,
            SMSBOX_HOST,
            SMSBOX_API_KEY,
        )
        result = await sms.send(
            SMS_RECIPIENT,
            SMS_MSG,
            SEND_MODE,
            {"strategy": SMSBOX_STRATEGY},
        )
        assert 0 == result


@pytest.mark.asyncio
async def test_ok_with_id(aresponses: Any) -> None:
    """Test result OK with a random ID."""
    # Get a random integer which will serve as the message ID
    msg_id = random.randint(100000000000, 999999999999)
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(
            text=f"OK {msg_id}",
            status=200,
        ),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(
            session,
            SMSBOX_HOST,
            SMSBOX_API_KEY,
        )
        result = await sms.send(
            SMS_RECIPIENT,
            SMS_MSG,
            SEND_MODE,
            {"strategy": SMSBOX_STRATEGY, "id": "1"},
        )
        assert msg_id == result


@pytest.mark.asyncio
async def test_credits(aresponses: Any) -> None:
    """Test credits async method returning a random number."""
    # Get a random float which will serve as the number of credits
    account_credits = round(random.uniform(0, 9999), 1)
    aresponses.add(
        "api.smsbox.pro",
        "/api.php",
        "post",
        aresponses.Response(
            text=f"CREDIT {account_credits}",
            status=200,
        ),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(
            session,
            SMSBOX_HOST,
            SMSBOX_API_KEY,
        )
        result = await sms.get_credits()
        assert account_credits == result


@pytest.mark.asyncio
async def test_exception_credits(aresponses: Any) -> None:
    """Test get_credits async method raising an exception."""
    aresponses.add(
        "api.smsbox.pro",
        "/api.php",
        "post",
        aresponses.Response(
            text="ERROR 02",
            status=200,
        ),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(
            session,
            SMSBOX_HOST,
            SMSBOX_API_KEY,
        )
        with pytest.raises(exceptions.SMSBoxException):
            await sms.get_credits()


@pytest.mark.asyncio
async def test_error_credits(aresponses: Any) -> None:
    """Test get_credits async method returning an unexpected string."""
    aresponses.add(
        "api.smsbox.pro",
        "/api.php",
        "post",
        aresponses.Response(
            text="FFF",
            status=200,
        ),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(
            session,
            SMSBOX_HOST,
            SMSBOX_API_KEY,
        )
        with pytest.raises(exceptions.SMSBoxException):
            await sms.get_credits()
