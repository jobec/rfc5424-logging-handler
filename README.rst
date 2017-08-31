Python rfc5424 syslog logging handler
=====================================

.. image:: https://img.shields.io/pypi/v/rfc5424-logging-handler.svg
    :target: https://pypi.python.org/pypi/rfc5424-logging-handler
.. image:: https://img.shields.io/pypi/pyversions/rfc5424-logging-handler.svg
    :target: https://pypi.python.org/pypi/rfc5424-logging-handler#downloads
.. image:: https://travis-ci.org/jobec/rfc5424-logging-handler.svg?branch=master
    :target: https://travis-ci.org/jobec/rfc5424-logging-handler
.. image:: https://codecov.io/github/jobec/rfc5424-logging-handler/coverage.svg?branch=master
    :target: https://codecov.io/github/jobec/rfc5424-logging-handler?branch=master

A more up-to-date, `RFC 5424 <https://tools.ietf.org/html/rfc5424>`_ compliant syslog handler for the Python logging framework

* Free software: BSD License
* Homepage: https://github.com/jobec/rfc5424-logging-handler

Features
--------

* `RFC 5424 <https://tools.ietf.org/html/rfc5424>`_ Compliant
* No need for complicated formatting strings

Installation
------------

Python package::

    pip install rfc5424-logging-handler


Usage
-----

Basics
~~~~~~

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
there are still syslog receivers that cannot handle it. To bypass this limitation, set the ``msg_as_utf8`` parameter
to ``False`` like this:

.. code-block:: python

    sh = Rfc5424SysLogHandler(address=('10.0.0.1', 514), msg_as_utf8=False)

Extended
~~~~~~~~

Full blown example:

.. code-block:: python

    import logging
    from rfc5424logging import Rfc5424SysLogHandler

    logger = logging.getLogger('syslogtest')
    logger.setLevel(logging.INFO)

    sh = Rfc5424SysLogHandler(
        address=('10.0.0.1', 514),
        hostname="overridden_server_name",
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

    <14>1 2020-01-01T05:10:20.841485+01:00 overridden_server_name my_wonderfull_app 555 some_unique_msgid [sd_id_1@32473 key1="value1"][sd_id2@32473 key3="value3" key2="value2"] \xef\xbb\xbfThis is an interesting message

With logger adapter
~~~~~~~~~~~~~~~~~~~

There's also an `LoggerAdapter` subclass available that makes it more easy to send structured data or a message ID with every message

.. code-block:: python

    import logging
    from rfc5424logging import Rfc5424SysLogHandler, Rfc5424SysLogAdapter

    logger = logging.getLogger('syslogtest')
    logger.setLevel(logging.INFO)

    sh = Rfc5424SysLogHandler(address=('10.0.0.1', 514))
    logger.addHandler(sh)
    adapter = Rfc5424SysLogAdapter(logger)

    msg_type = 'interesting'
    adapter.info('This is an %s message',
                 msg_type, structured_data={'sd_id2': {'key2': 'value2', 'key3': 'value3'}})
    adapter.info('This is an %s message', msg_type, msgid='some_unique_msgid')
    adapter.info('This is an %s message',
                 msg_type,
                 structured_data={'sd_id2': {'key2': 'value2', 'key3': 'value3'}}, msgid='some_unique_msgid')

    # Since version 1.0 it's also possible to override the appname, hostname and procid per message
    adapter.info('Some other message',
                 msgid='some_unique_msgid', appname="custom_appname",
                 hostname="my_hostname", procid="5678")

Using a logging config dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
                'hostname': 'overridden_server_name',
                'enterprise_id': 32473,
                'appname': 'my_wonderfull_app',
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

Prevent a field from being sent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want the appname, hostname or procid field to be empty, instead of it being determined automatically, set it to
NILVALUE explicitly. Setting it to `None` or an empty string will cause it to be filled automatically.

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

    <14>1 2020-01-01T05:10:20.841485+01:00 - - - - - My syslog message

