Installation
============

Install the package with pip::

    pip install rfc5424-logging-handler

Usage
=====

Basic example
-------------

After installing you can use this package like this:

.. code-block:: python

    import logging
    from rfc5424logging import Rfc5424SysLogHandler

    logger = logging.getLogger('syslogtest')
    logger.setLevel(logging.INFO)

    sh = Rfc5424SysLogHandler(address=('10.0.0.1', 514))
    logger.addHandler(sh)

    msg_type = 'interesting'
    logger.info('This is an %s message', msg_type)

This will send the following message to the syslog server::

    <14>1 2020-01-01T05:10:20.841485+01:00 myserver syslogtest 5252 - - \xef\xbb\xbfThis is an interesting message

Note the UTF8 Byte order mark (BOM) preceding the message. While required by
`RFC 5424 section 6.4 <https://tools.ietf.org/html/rfc5424#section-6.4>`_ if the message is known to be UTF-8 encoded,
there are still syslog receivers that cannot handle it. To bypass this limitation, when initializing the handler Class,
set the ``msg_as_utf8`` parameter to ``False`` like this:

.. code-block:: python

    sh = Rfc5424SysLogHandler(address=('10.0.0.1', 514), msg_as_utf8=False)

Sending RFC5424 specific fields
-------------------------------

The example below sets as many RFC5424 specific fields as possible.
If one of the fields isn't specified, a default value or the NIL value is used.

+-----------------+---------------------------------------------------+
| RFC5424 Field   | Default value                                     |
+=================+===================================================+
| hostname        | Value of ``socket.gethostname()``                 |
+-----------------+---------------------------------------------------+
| appname         | Name of the logger                                |
+-----------------+---------------------------------------------------+
| procid          | ``process`` attribute of the log record.          |
|                 | Normally the process ID of the python application |
+-----------------+---------------------------------------------------+
| structured_data | NIL                                               |
+-----------------+---------------------------------------------------+
| enterprise_id   | None (and raises an error when sending            |
|                 | structured data without enterprise ID)            |
+-----------------+---------------------------------------------------+
| msgid           | NIL                                               |
+-----------------+---------------------------------------------------+

Notice that the structured data field can be specified twice. Once when
initiating the log handler (for structured data that's sent with every message)
and once when sending the message (for structured data specific to this message).

.. code-block:: python

    import logging
    from rfc5424logging import Rfc5424SysLogHandler

    logger = logging.getLogger('syslogtest')
    logger.setLevel(logging.INFO)

    sh = Rfc5424SysLogHandler(
        address=('10.0.0.1', 514),
        hostname="otherserver",
        appname="my_wonderfull_app",
        procid=555,
        structured_data={'sd_id_1': {'key1': 'value1'}},
        enterprise_id=32473
    )
    logger.addHandler(sh)

    msg_type = 'interesting'
    extra = {
        'msgid': 'some_unique_msgid',
        'structured_data': {
            'sd_id2': {'key2': 'value2', 'key3': 'value3'}
        }
    }
    logger.info('This is an %s message', msg_type, extra=extra)

That will send the following message to the syslog server::

    <14>1 2020-01-01T05:10:20.841485+01:00 otherserver my_wonderfull_app 555 some_unique_msgid [sd_id_1@32473 key1="value1"][sd_id2@32473 key3="value3" key2="value2"] \xef\xbb\xbfThis is an interesting message

If you want the appname, hostname or procid field to be empty, instead of it being determined automatically,
set it to ``NILVALUE`` explicitly. Setting it to ``None`` or an empty string will cause it to be filled automatically.

.. code-block:: python

    import logging
    from rfc5424logging import Rfc5424SysLogHandler, NILVALUE

    logger = logging.getLogger('syslogtest')
    logger.setLevel(logging.INFO)

    sh = Rfc5424SysLogHandler(
        address=('10.0.0.1', 514),
        hostname=NILVALUE,
        appname=NILVALUE,
        procid=NILVALUE,
    )
    logger.addHandler(sh)

    logger.info('My syslog message')

    msg_type = 'interesting'
    extra = {
        'msgid': 'some_unique_msgid',
        'structured_data': {
            'sd_id2': {'key2': 'value2', 'key3': 'value3'}
        }
    }
    logger.info('This is an %s message', msg_type, extra=extra)

That will send the following message to the syslog server::

    <14>1 2020-01-01T05:10:20.841485+01:00 - - - - - \xef\xbb\xbfMy syslog message

Log in UTC time
---------------

Sometimes you have log sources all over the world in different timezones.
In such a case it's sometimes easier to have all you timestamps in the UTC timezone.

You can enable this by setting the ``utc_timestamp`` argument to ``True`` like this.

.. code-block:: python

    from rfc5424logging import Rfc5424SysLogHandler

    sh = Rfc5424SysLogHandler(
        address=('10.0.0.1', 514),
        utc_timestamp=True
    )

TLS/SSL syslog connection
-------------------------

Sometimes logs contain sensitive date and shouldn't go over the network in plain text.
For this, you can setup a TLS/SSL connection to the syslog server with the following example.

Check out the code the the ``Rfc5424SysLogHandler`` class for more options.

.. code-block:: python

    import logging
    from rfc5424logging import Rfc5424SysLogHandler

    logger = logging.getLogger('syslogtest')
    logger.setLevel(logging.INFO)

    sh = Rfc5424SysLogHandler(
        address=('10.0.0.1', 514),
        tls_enable=True,
        tls_verify=True,
        tls_ca_bundle="/path/to/ca-bundle.pem"
    )
    logger.addHandler(sh)

    msg_type = 'interesting'
    logger.info('This is an %s message', msg_type)


Using a logging config dictionary
---------------------------------

Python supports `configuring the logging system from a dictionary <https://docs.python.org/3/howto/logging-cookbook.html#an-example-dictionary-based-configuration>`_.
Below is an example using the rfc5424 log handler to log to syslog and the stream handler to log to console.

.. code-block:: python

    import logging
    import logging.config

    log_settings = {
        'version': 1,
            'formatters': {
            'console': {
                'format': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'console'
            },
            'syslog': {
                'level': 'INFO',
                'class': 'rfc5424logging.handler.Rfc5424SysLogHandler',
                'address': ('127.0.0.1', 514),
                'enterprise_id': 32473,
                'structured_data': {'sd_id_1': {'key1': 'value1'}},
            },
        },
        'loggers': {
            'syslogtest': {
                'handlers': ['console', 'syslog'],
                'level': 'DEBUG',
             },
        }
    }
    logging.config.dictConfig(log_settings)

    logger = logging.getLogger('syslogtest')
    logger.info('This message appears on console and is sent to syslog')
    logger.debug('This debug message appears on console only')

Logger adapter
--------------

There's also an ``LoggerAdapter`` subclass available that makes it easier to send
structured data and a message ID or to override fields with every message.

.. code-block:: python

    import logging
    from rfc5424logging import Rfc5424SysLogHandler, Rfc5424SysLogAdapter

    logger = logging.getLogger('syslogtest')
    logger.setLevel(logging.INFO)

    sh = Rfc5424SysLogHandler(address=('10.0.0.1', 514))
    logger.addHandler(sh)
    adapter = Rfc5424SysLogAdapter(logger)

    adapter.info('This is an interesting message',
                 structured_data={'sd_id2': {'key2': 'value2', 'key3': 'value3'}})

    adapter.info('This is an interesting message',
                 msgid='some_unique_msgid')

    adapter.info('This is an interesting message',
                 structured_data={'sd_id2': {'key2': 'value2', 'key3': 'value3'}},
                 msgid='some_unique_msgid')

    # Since version 1.0 it's also possible to override the appname, hostname and procid per message
    adapter.info('Some other message',
                 msgid='some_unique_msgid',
                 appname="custom_appname",
                 hostname="my_hostname",
                 procid="5678")
