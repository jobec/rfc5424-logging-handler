Changelog
---------

`1.4.0`_ - 2019/01/30
~~~~~~~~~~~~~~~~~~~~~

**Added**

* `#27`_ Make it possible to log to streams as an alternate transport.
* Added API documentation.

**Changed**

* Syslog facilities and framing options have moved from the ``RfcSysLogHandler`` class
  to module level variables. **You may have to adjust your references to them.**

`1.3.0`_ - 2018/10/19
~~~~~~~~~~~~~~~~~~~~~

**Added**

* `#23`_ Add support for TLS/SSL

`1.2.1`_ - 2018/09/21
~~~~~~~~~~~~~~~~~~~~~

**Fixed**

* `#21`_ Registered structured data IDs where also suffixed with an enterprise ID.

**Added**

* `#22`_ Add ``utc_timestamp`` parameter to allow logging in UTC time.

`1.1.2`_ - 2018/02/03
~~~~~~~~~~~~~~~~~~~~~

**Fixed**

* `#15`_ When logging to ``/dev/log`` with python 2.7, the connection was permanently lost when the local syslog server
  was restarted.
* `#16`_ The ``extra`` info of a message did not overwrite that of the logging adapter instance.

`1.1.1`_ - 2017/12/08
~~~~~~~~~~~~~~~~~~~~~

**Fixed**

* `#14`_ Fixed handling of ``extra`` parameter in logging adapter.

`1.1.0`_ - 2017/11/24
~~~~~~~~~~~~~~~~~~~~~

**Added**

* The ``msg`` parameter for the logger handler can now be absent allowing "structured data only" messages.

**Fixed**

* Correct the automatic value of the ``hostname`` when the value is anything other then ``NILVALUE``
* The syslog message is now empty in conformance with RFC5424 when it's value is ``None`` or an empty string.


`1.0.3`_ - 2017/10/08
~~~~~~~~~~~~~~~~~~~~~

No functional changes. Only documentation was changed.

**Added**

* Logstash configuration example for RFC5424.

**Changed**

* Moved most of the documentation out of the readme file.

`1.0.2`_ - 2017/08/31
~~~~~~~~~~~~~~~~~~~~~

**Fixed**

* Package description rendering on PyPi due to bug `pypa/wheel#189 <https://github.com/pypa/wheel/issues/189>`_

`1.0.1`_ - 2017/08/30
~~~~~~~~~~~~~~~~~~~~~

**Added**

* `#12`_: It's now possible to send syslog messages as `MSG-ANY <https://tools.ietf.org/html/rfc5424#section-6>`_
  which suppresses the UTF-8 byte order mark (BOM) when sending messages.

`1.0.0`_ - 2017/05/30
~~~~~~~~~~~~~~~~~~~~~

**Changed**

* `#10`_: Procid, appname and hostname can now be set per message, both with the handler as well as with the adapter

.. note::
   This release has a slight change in behaviour. Setting one of the appnama, hostname of procid message to None or an
   empty string will cause it to be filled in automatically. Previously, setting it to an empty string caused it to
   be set to NILVALUE (a - ). You now need to set it explicilty to NILVALUE if you want to omit it from the message.

`0.2.0`_ - 2017/01/27
~~~~~~~~~~~~~~~~~~~~~

**Fixed**

* Better input handling
* Better sanitizing of invalid input

`0.1.0`_ - 2017/01/22
~~~~~~~~~~~~~~~~~~~~~

**Added**

* `#4`_: Adapter class to make it easier to log message IDs or structured data
* Logging of EMERGENCY, ALERT and NOTICE syslog levels by using the adapter class
* Extensive test suite

`0.0.2`_ - 2017/01/18
~~~~~~~~~~~~~~~~~~~~~

**Added**

* `#5`_ Introduced Python 2.7 compatibility

0.0.1 - 2017/01/11
~~~~~~~~~~~~~~~~~~

* Initial release

.. _1.4.0: https://github.com/jobec/rfc5424-logging-handler/compare/1.3.0...1.4.0
.. _1.3.0: https://github.com/jobec/rfc5424-logging-handler/compare/1.2.1...1.3.0
.. _1.2.1: https://github.com/jobec/rfc5424-logging-handler/compare/1.1.2...1.2.1
.. _1.1.2: https://github.com/jobec/rfc5424-logging-handler/compare/1.1.1...1.1.2
.. _1.1.1: https://github.com/jobec/rfc5424-logging-handler/compare/1.1.0...1.1.1
.. _1.1.0: https://github.com/jobec/rfc5424-logging-handler/compare/1.0.3...1.1.0
.. _1.0.3: https://github.com/jobec/rfc5424-logging-handler/compare/1.0.2...1.0.3
.. _1.0.2: https://github.com/jobec/rfc5424-logging-handler/compare/1.0.1...1.0.2
.. _1.0.1: https://github.com/jobec/rfc5424-logging-handler/compare/1.0.0...1.0.1
.. _1.0.0: https://github.com/jobec/rfc5424-logging-handler/compare/0.2.0...1.0.0
.. _0.2.0: https://github.com/jobec/rfc5424-logging-handler/compare/0.1.0...0.2.0
.. _0.1.0: https://github.com/jobec/rfc5424-logging-handler/compare/0.0.2...0.1.0
.. _0.0.2: https://github.com/jobec/rfc5424-logging-handler/compare/0.0.1...0.0.2

.. _#27: https://github.com/jobec/rfc5424-logging-handler/issues/27
.. _#23: https://github.com/jobec/rfc5424-logging-handler/issues/23
.. _#22: https://github.com/jobec/rfc5424-logging-handler/issues/22
.. _#21: https://github.com/jobec/rfc5424-logging-handler/issues/21
.. _#16: https://github.com/jobec/rfc5424-logging-handler/pull/16
.. _#15: https://github.com/jobec/rfc5424-logging-handler/issues/15
.. _#14: https://github.com/jobec/rfc5424-logging-handler/pull/14
.. _#12: https://github.com/jobec/rfc5424-logging-handler/pull/12
.. _#10: https://github.com/jobec/rfc5424-logging-handler/pull/10
.. _#5: https://github.com/jobec/rfc5424-logging-handler/issues/5
.. _#4: https://github.com/jobec/rfc5424-logging-handler/pull/4
