"""Example script."""

import asyncio
import sys
from os import getenv

import aiohttp

from pysmsboxnet import exceptions
from pysmsboxnet.api import Client


async def main():
    """Run the example."""
    async with aiohttp.ClientSession() as session:
        sms = Client(session, "api.smsbox.pro", API_KEY)

        try:
            # To send a message
            # define the strategy in the dict passed as the last parameter
            # also ask the API to return the ID of the sent message
            # by setting the id parameter to 1
            # if id is not set, the send function will return 0
            # on failure, an exception is raised
            # Uncomment it if you need it
            # msgID = await sms.send(
            #     SMS_RECIPIENT, "Test message.", "expert", {"strategy": "2", "id": "1"}
            # )
            # Print confirmation and the message ID
            # print(f"SMS sent, ID : {msgID}")

            # Get the remaining credits
            remaining_credits = await sms.get_credits()
            # print(f"Remaining credits: {remaining_credits}")
            if remaining_credits > 0:
                print("There are remaining credits")
            else:
                print("No remaining credits")
        except exceptions.SMSBoxException as e:
            print(f"Exception: {e}")


# Get API key from environment variable
API_KEY = getenv("SMSBOX_API_KEY", "nokey")
SMS_RECIPIENT = "9990001"

if API_KEY == "nokey":
    print("No key specified, exiting")
    sys.exit(1)

asyncio.run(main())
