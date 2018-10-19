Python rfc5424 syslog logging handler
=====================================

.. image:: https://readthedocs.org/projects/rfc5424-logging-handler/badge/?version=latest
    :target: https://rfc5424-logging-handler.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/rfc5424-logging-handler.svg
    :target: https://pypi.python.org/pypi/rfc5424-logging-handler
.. image:: https://img.shields.io/pypi/pyversions/rfc5424-logging-handler.svg
    :target: https://pypi.python.org/pypi/rfc5424-logging-handler#downloads
.. image:: https://travis-ci.org/jobec/rfc5424-logging-handler.svg?branch=master
    :target: https://travis-ci.org/jobec/rfc5424-logging-handler
.. image:: https://codecov.io/github/jobec/rfc5424-logging-handler/coverage.svg?branch=master
    :target: https://codecov.io/github/jobec/rfc5424-logging-handler?branch=master

An up-to-date, `RFC 5424 <https://tools.ietf.org/html/rfc5424>`_ compliant syslog handler for the Python logging framework.

* Free software: BSD License
* Homepage: https://github.com/jobec/rfc5424-logging-handler
* Documentation: http://rfc5424-logging-handler.readthedocs.org/

Features
--------

* `RFC 5424 <https://tools.ietf.org/html/rfc5424>`_ Compliant.
* Python Logging adapter for easier sending of rfc5424 specific fields.
* No need for complicated formatting strings.
* TLS/SSL syslog support.

Installation
------------

Python package::

    pip install rfc5424-logging-handler

Usage
-----

After installing you can use this package like this:

.. code-block:: python

    import logging
    from rfc5424logging import Rfc5424SysLogHandler

    logger = logging.getLogger('syslogtest')
    logger.setLevel(logging.INFO)

    sh = Rfc5424SysLogHandler(address=('10.0.0.1', 514))
    logger.addHandler(sh)

    logger.info('This is an interesting message', extra={'msgid': 'some_unique_msgid'})

This will send the following message to the syslog server::

    <14>1 2020-01-01T05:10:20.841485+01:00 myserver syslogtest 5252 some_unique_msgid - \xef\xbb\xbfThis is an interesting message

Note the UTF8 Byte order mark (BOM) preceding the message. While required by
`RFC 5424 section 6.4 <https://tools.ietf.org/html/rfc5424#section-6.4>`_ if the message is known to be UTF-8 encoded,
there are still syslog receivers that cannot handle it. To bypass this limitation, when initializing the handler Class,
set the ``msg_as_utf8`` parameter to ``False`` like this:

.. code-block:: python

    sh = Rfc5424SysLogHandler(address=('10.0.0.1', 514), msg_as_utf8=False)

For more examples, have a look at the `documentation <http://rfc5424-logging-handler.readthedocs.org/>`_
