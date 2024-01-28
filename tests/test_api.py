"""Tests for pysmsboxnet."""

from __future__ import annotations

import random
from typing import Any

import aiohttp
import pytest
from pysmsboxnet import exceptions
from pysmsboxnet.api import Client

# Constants
SMSBOX_HOST = "api.smsbox.pro"
SMSBOX_API_KEY = "pub-xxxxx-xxxxx-xxxx-xxxx-xxxxx-xxxxxxxx"
SMS_RECIPIENT = "9999001"
SMS_MSG = "Test d'un message ! En plus il va être envoyé."
SEND_MODE = "expert"
SMSBOX_STRATEGY = "2"


@pytest.mark.asyncio
async def test_parameters_error(aresponses: Any) -> None:
    """Test if exception is raised if web server returns ERROR 01."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(
            text="ERROR 01",
            status=200,
        ),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(session, SMSBOX_HOST, SMSBOX_API_KEY)
        with pytest.raises(exceptions.ParameterErrorException):
            await sms.send(
                SMS_RECIPIENT,
                SMS_MSG,
                SEND_MODE,
                {"strategy": SMSBOX_STRATEGY},
            )
            await session.close()


@pytest.mark.asyncio
async def test_bad_auth(aresponses: Any) -> None:
    """Test if exception is raised in case of wrong authentication ERROR 02."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
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
        with pytest.raises(exceptions.AuthException):
            await sms.send(
                SMS_RECIPIENT,
                SMS_MSG,
                SEND_MODE,
                {"strategy": SMSBOX_STRATEGY},
            )
            await session.close()


@pytest.mark.asyncio
async def test_billing(aresponses: Any) -> None:
    """Test if BillingException is raised in case of ERROR 03."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(
            text="ERROR 03",
            status=200,
        ),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(
            session,
            SMSBOX_HOST,
            SMSBOX_API_KEY,
        )
        with pytest.raises(exceptions.BillingException):
            await sms.send(
                SMS_RECIPIENT,
                SMS_MSG,
                SEND_MODE,
                {"strategy": SMSBOX_STRATEGY},
            )
            await session.close()


@pytest.mark.asyncio
async def test_bad_dest(aresponses: Any) -> None:
    """Test if WrongRecipientException is raised on ERROR 04."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(
            text="ERROR 04",
            status=200,
        ),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(
            session,
            SMSBOX_HOST,
            SMSBOX_API_KEY,
        )
        with pytest.raises(exceptions.WrongRecipientException):
            await sms.send(
                SMS_RECIPIENT,
                SMS_MSG,
                SEND_MODE,
                {"strategy": SMSBOX_STRATEGY},
            )
            await session.close()


@pytest.mark.asyncio
async def test_internal_error(aresponses: Any) -> None:
    """Test if right exception is raised on ERROR 05."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(
            text="ERROR 05",
            status=200,
        ),
    )
    async with aiohttp.ClientSession() as session:
        sms = Client(
            session,
            SMSBOX_HOST,
            SMSBOX_API_KEY,
        )
        with pytest.raises(exceptions.InternalErrorException):
            await sms.send(
                SMS_RECIPIENT,
                SMS_MSG,
                SEND_MODE,
                {"strategy": SMSBOX_STRATEGY},
            )
            await session.close()


@pytest.mark.asyncio
async def test_other_error(aresponses: Any) -> None:
    """Test unknown error."""
    aresponses.add(
        "api.smsbox.pro",
        "/1.1/api.php",
        "post",
        aresponses.Response(
            text="ERROR",
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
            await sms.send(
                SMS_RECIPIENT,
                SMS_MSG,
                SEND_MODE,
                {"strategy": SMSBOX_STRATEGY},
            )
            await session.close()


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
            await session.close()


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
        await session.close()


@pytest.mark.asyncio
async def test_ok_with_id(aresponses: Any) -> None:
    """Test result OK with a random ID."""
    # Get a random integer which will serv as the message ID
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
        await session.close()


@pytest.mark.asyncio
async def test_credits(aresponses: Any) -> None:
    """Test credits async property returning a random number."""
    # Get a random float which will serv as the number of credits
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
        await session.close()


@pytest.mark.asyncio
async def test_exception_credits(aresponses: Any) -> None:
    """Test get credits async property raising exception."""
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
            await session.close()


@pytest.mark.asyncio
async def test_error_credits(aresponses: Any) -> None:
    """Test get credits async property returning strange string."""
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
            await session.close()
