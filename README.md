# pysmsboxnet

Asynchronous Python library for [smsbox.net](https://www.smsbox.net) API.
Currently it allows to send a SMS, using the [v1.1 API](https://en.smsbox.net/docs/doc-API-SMSBOX-1.1-EN.html).
You can also [download the documentation](https://en.smsbox.net/docs/doc-API-SMSBOX-1.1-EN.pdf).
Future version might allow to use other [account features](https://en.smsbox.net/docs/doc-APIFunctions-SMSBOX-FR.html), this doc is in French.
The exception is the credits async property which allows getting remaining credits.

## How to use

See [example.py](/example.py).
The `pysmsboxnet.net.api.Client` has the following methods:

- Constructor which takes the following arguments:
  - session: an instance of aiohttp.ClientSession
  - host (str): the SMSBox API endpoint I.E. `https://api.smsbox.pro`
  - cleApi (str): your smsbox.net API key, [see API documentation](https://en.smsbox.net/docs/doc-API-SMSBOX-1.1-EN.html); name is in French to reflect API documentation
  - timeout (int, optional, default 30
- Send (return int: 0 or ID of sent SMS if applicable)
  - dest (str): the SMS recipient, see API documentation about how to format
  - msg (str): your message
  - mode (str): same as mode in the API documentation
  - parameters (dict): to add other API parameters, for example the minimum to add is `strategy`
- credits: async property which returns remaining credits as float

Exceptions are implemented and thrown: `pysmsboxnet.exceptions.ParameterErrorException`, `pysmsboxnet.exceptions.AuthException`, `pysmsboxnet.exceptions.BillingException`, `pysmsboxnet.exceptions.WrongRecipientException`, `pysmsboxnet.exceptions.InternalErrorException`, `pysmsboxnet.exceptions.HTTPException`.
In case of an unknown exception, `pysmsboxnet.exceptions.SMSBoxException` is thrown.
