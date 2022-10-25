"""Tests for pysmsboxnet"""

import asyncio
import aiohttp
import pytest
from unittest.mock import patch
from pysmsboxnet.api import Client
from pysmsboxnet import exceptions


@pytest.mark.asyncio
async def test_parameters_error(aresponses):
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
        sms = Client(session, "https://api.smsbox.pro", "pub-xxxxxxxx")
        with pytest.raises(exceptions.ParameterErrorException):
            await sms.send(
                "9999001",
                "Test d'un message ! En plus il va être envoyé.",
                "expert",
                {"strategy": "2"},
            )
            await session.close()


@pytest.mark.asyncio
async def test_bad_auth(aresponses):
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
            "https://api.smsbox.pro",
            "pub-xxxxx-xxxxx-xxxx-xxxx-xxxxx-xxxxxxxx",
        )
        with pytest.raises(exceptions.AuthException):
            await sms.send(
                "9999001",
                "Test d'un message ! En plus il va être envoyé.",
                "expert",
                {"strategy": "2"},
            )
            await session.close()


@pytest.mark.asyncio
async def test_billing(aresponses):
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
            "https://api.smsbox.pro",
            "pub-xxxxx-xxxxx-xxxx-xxxx-xxxxx-xxxxxxxx",
        )
        with pytest.raises(exceptions.BillingException):
            await sms.send(
                "9999001",
                "Test d'un message ! En plus il va être envoyé.",
                "expert",
                {"strategy": "2"},
            )
            await session.close()


@pytest.mark.asyncio
async def test_bad_dest(aresponses):
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
            "https://api.smsbox.pro",
            "pub-xxxxx-xxxxx-xxxx-xxxx-xxxxx-xxxxxxxx",
        )
        with pytest.raises(exceptions.WrongRecipientException):
            await sms.send(
                "9999001",
                "Test d'un message ! En plus il va être envoyé.",
                "expert",
                {"strategy": "2"},
            )
            await session.close()


@pytest.mark.asyncio
async def test_internal_error(aresponses):
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
            "https://api.smsbox.pro",
            "pub-xxxxx-xxxxx-xxxx-xxxx-xxxxx-xxxxxxxx",
        )
        with pytest.raises(exceptions.InternalErrorException):
            await sms.send(
                "9999001",
                "Test d'un message ! En plus il va être envoyé.",
                "expert",
                {"strategy": "2"},
            )
            await session.close()


@pytest.mark.asyncio
async def test_other_error(aresponses):
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
            "https://api.smsbox.pro",
            "pub-xxxxx-xxxxx-xxxx-xxxx-xxxxx-xxxxxxxx",
        )
        with pytest.raises(exceptions.SMSBoxException):
            await sms.send(
                "9999001",
                "Test d'un message ! En plus il va être envoyé.",
                "expert",
                {"strategy": "2"},
            )
            await session.close()


@pytest.mark.asyncio
async def test_http_error(aresponses):
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
            "https://api.smsbox.pro",
            "pub-xxxxx-xxxxx-xxxx-xxxx-xxxxx-xxxxxxxx",
        )
        with pytest.raises(exceptions.HTTPException):
            await sms.send(
                "9999001",
                "Test d'un message ! En plus il va être envoyé.",
                "expert",
                {"strategy": "2"},
            )
            await session.close()
