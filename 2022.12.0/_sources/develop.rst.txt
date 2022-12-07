Add features to pysmsboxnet
===========================

To implement a new API feature, add a new method which will call the following private method:

.. autofunction:: pysmsboxnet.api.Client.__smsbox_request

If an exception is needed, put it in pysmsboxnet/exceptions.py and make it extend :py:class:`pysmsboxnet.exceptions.SMSBoxException`.
