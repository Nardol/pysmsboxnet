import asyncio
from os import getenv
from sys import exit

import aiohttp

from pysmsboxnet import exceptions
from pysmsboxnet.api import Client


async def main():
    async with aiohttp.ClientSession() as session:
        sms = Client(session, "https://api.smsbox.pro", API_KEY)

        try:
            msgID = await sms.send(
                SMS_RECIPIENT, "Test message.", "expert", {"strategy": "2", "id": "1"}
            )
            print(f"SMS sent, ID : {msgID}")
        except exceptions.SMSBoxException as e:
            print(f"As expected, exception: {e}")
            await session.close()


# Get API key from environment variable
API_KEY = getenv("SMSBOX_API_KEY", "nokey")
SMS_RECIPIENT = "9990001"

if API_KEY == "nokey":
    print("No key specified, exiting")
    exit(1)

asyncio.run(main())
