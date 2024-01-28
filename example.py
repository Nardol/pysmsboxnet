"""Example script."""

import asyncio
from os import getenv
from sys import exit

import aiohttp
from pysmsboxnet import exceptions
from pysmsboxnet.api import Client


async def main():
    """Execute main instructions."""
    async with aiohttp.ClientSession() as session:
        sms = Client(session, "api.smsbox.pro", API_KEY)

        try:
            # To send a message
            # we define the strategy in the dict passed as last parameter
            # In this dict, we also ask the API to return the ID of message sent
            # With the parameter id set to 1
            # If we don't set id, the send function will return 0
            # In case of failure an exception will be thrown
            # Uncomment it if you need it
            # msgID = await sms.send(
            #     SMS_RECIPIENT, "Test message.", "expert", {"strategy": "2", "id": "1"}
            # )
            # We display the message is sent and its ID
            # print(f"SMS sent, ID : {msgID}")

            # We get remaining credits
            remaining_credits = await sms.get_credits()
            # print(f"Remaining credits: {remaining_credits}")
            if remaining_credits > 0:
                print("There are remaining credits")
            else:
                print("No remaining credit")
        except exceptions.SMSBoxException as e:
            print(f"Exception: {e}")
            await session.close()


# Get API key from environment variable
API_KEY = getenv("SMSBOX_API_KEY", "nokey")
SMS_RECIPIENT = "9990001"

if API_KEY == "nokey":
    print("No key specified, exiting")
    exit(1)

asyncio.run(main())
