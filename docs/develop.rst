Add features to pysmsboxnet
===========================

To implement a new API feature, add a new method that calls the following private method:

.. automethod:: pysmsboxnet.api.Client._smsbox_request

If an exception is needed, place it in ``pysmsboxnet/exceptions.py`` and have it extend :py:class:`pysmsboxnet.exceptions.SMSBoxException`.
