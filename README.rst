Python rfc5424 syslog logging handler
=====================================

.. image:: https://img.shields.io/pypi/v/rfc5424-logging-handler.svg
    :target: https://pypi.python.org/pypi/rfc5424-logging-handler
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

After installing you can use this package like this:

.. code-block:: python

    import logging
    from rfc5424logging import Rfc5424SysLogHandler

    logger = logging.getLogger('systlogtest')
    logger.setLevel(logging.INFO)

    sh = Rfc5424SysLogHandler(address=('10.0.0.1', 514))
    logger.addHandler(sh)

    msg_type = 'interesting'
    logger.info('This is an %s message', msg_type)

This will send the following message to the syslog server::

    <14>1 2020-01-01T05:10:20.841485+01:00 myserver syslogtest 5252 - - This is an interesting message