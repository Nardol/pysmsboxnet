# pysmsboxnet

Asynchronous Python library for [smsbox.net](https://www.smsbox.net) API.
Currently it only allows to send a SMS, using the [v1.1 API](https://en.smsbox.net/docs/doc-API-SMSBOX-1.1-EN.html).
You can also [download the documentation](https://en.smsbox.net/docs/doc-API-SMSBOX-1.1-EN.pdf).
Future version might allow to use the [account features](https://en.smsbox.net/docs/doc-APIFunctions-SMSBOX-FR.html), this doc is in French.

## How to use

See [example.py](/example.py).
The `pysmsboxnet.net.api.Client` has the following methods:

- Constructor which takes the following arguments:
  - session: an instance of aiohttp.ClientSession
  - host (str): the SMSBox API endpoint I.E. `https://api.smsbox.pro`
  - cleApi (str): your smsbox.net API key, [see API documentation](https://en.smsbox.net/docs/doc-API-SMSBOX-1.1-EN.html); name is in French to reflect API documentation
  - timeout (int, optional, default 30
- Send
  - dest (str): the SMS recipient, see API documentation about how to format
  - msg (str): your message
  - mode (str): same as mode in the API documentation
  - parameters (dict): to add other API parameters, for example the main to add is `strategy`

Exceptions are implemented and thrown: `ParameterErrorException`, `AuthException`, `BillingException`, `WrongRecipientException`, `InternalErrorException`, `HTTPException`.
In case of an unknown exception, `SMSBoxException` is thrown.
