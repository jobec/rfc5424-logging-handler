Changelog
---------

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
   This release has a slight change in behaviour. Setting one of the appnama, hostname of procid message to None of an
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

.. _1.0.2: https://github.com/jobec/rfc5424-logging-handler/compare/1.0.1...1.0.2
.. _1.0.1: https://github.com/jobec/rfc5424-logging-handler/compare/1.0.0...1.0.1
.. _1.0.0: https://github.com/jobec/rfc5424-logging-handler/compare/0.2.0...1.0.0
.. _0.2.0: https://github.com/jobec/rfc5424-logging-handler/compare/0.1.0...0.2.0
.. _0.1.0: https://github.com/jobec/rfc5424-logging-handler/compare/0.0.2...0.1.0
.. _0.0.2: https://github.com/jobec/rfc5424-logging-handler/compare/0.0.1...0.0.2

.. _#12: https://github.com/jobec/rfc5424-logging-handler/pull/12
.. _#10: https://github.com/jobec/rfc5424-logging-handler/pull/10
.. _#5: https://github.com/jobec/rfc5424-logging-handler/issues/5
.. _#4: https://github.com/jobec/rfc5424-logging-handler/pull/4
