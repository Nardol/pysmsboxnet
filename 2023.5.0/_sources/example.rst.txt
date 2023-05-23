Usage example
=============

The following example can be found on the `GitHub repository <https://github.com/Nardol/pysmsboxnet>`_.
Even if it is a little bit different, its principle is the same.

..  code-block:: python

   import asyncio
   from sys import exit

   import aiohttp

   from pysmsboxnet import exceptions
   from pysmsboxnet.api import Client


   async def main():
       async with aiohttp.ClientSession() as session:
       # After initializing a AIOHTTP client session, we initialize a Client object
           sms = Client(session, "api.smsbox.pro", API_KEY)

           try:
               # Before sending a message, we display remaining credits
               credits = await sms.get_credits()
               print(f"Remaining credits before: {credits}")

               # To send a message
               # we define the strategy in the dict passed as last parameter
               # In this dict, we also ask the API to return the ID of message sent
               # With the parameter id set to 1
               # If we don't set id, the send function will return 0
               # In case of failure an exception will be thrown
               msgID = await sms.send(
                   SMS_RECIPIENT, "Test message.", "expert", {"strategy": "2", "id": "1"}
               )
               # We display the message is sent and the ID
               print(f"SMS sent, ID : {msgID}")

               # We get remaining credits
               credits = await sms.get_credits()
               print(f"Remaining credits after: {credits}")
               if credits > 0:
                   print("There are remaining credits")
               else:
                   print("No remaining credit")
           except exceptions.SMSBoxException as e:
               print(f"Exception: {e}")
               await session.close()


   # Specify the API key
   API_KEY = "xxx"
   SMS_RECIPIENT = "9990001" # a sandbox number for a succeffull 0.5 credit SMS

   asyncio.run(main())

This example shows all actual possibilities of this libraries.
If you want to add more, go to the next section.
