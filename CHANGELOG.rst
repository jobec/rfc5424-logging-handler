Changelog
---------

1.0.0 (2017-05-30)
~~~~~~~~~~~~~~~~~~

* Procid, appname and hostname can now be set per message, both with the handler as well as with the adapter

.. note::
   This release has a slight change in behaviour. Setting one of the appnama, hostname of procid message to None of an
   empty string will cause it to be filled in automatically. Previously, setting it to an empty string caused it to
   be set to NILVALUE (a - ). You now need to set it explicilty to NILVALUE if you want to omit it from the message.

0.2.0 (2017-01-27)
~~~~~~~~~~~~~~~~~~

* Better input handling
* Better sanitizing of invalid input

0.1.0 (2017-01-22)
~~~~~~~~~~~~~~~~~~

* Adapter class to make it easier to log message IDs or structured data
* Logging of EMERGENCY, ALERT and NOTICE syslog levels by using the adapter class
* Extensive test suite

0.0.2 (2017-01-18)
~~~~~~~~~~~~~~~~~~

* Introduced Python 2.7 compatibility

0.0.1 (2017-01-11)
~~~~~~~~~~~~~~~~~~

* Initial release
