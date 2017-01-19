import logging

from handler import NILVALUE


class Rfc5424SysLogLogger(logging.Logger):
    """
    A Logger class which takes in additional information related to the RFC 5424 Syslog Protocol
    (ie. msgid and structured_data), and passes it into the standard logging.Logger class as part of the extras
    argument in the _log method.

    This class overrides the following methods from logging.logger, which call the _log method:
        - debug
        - info
        - warning
        - error
        - critical
        - log
    """

    def __init__(self, name, level=logging.NOTSET):
        super(Rfc5424SysLogLogger, self).__init__(name, level)

    def debug(self, msg, msgid=NILVALUE, structured_data=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        Args:
            msg:
                Message to log
            msgid:
                RFC 5424 MSGID
            structured_data:
                RFC 5424 STRUCTURED-DATA
        """
        if structured_data is None:
            structured_data = {}
        self._update(msgid, structured_data, kwargs)
        super(Rfc5424SysLogLogger, self).debug(msg, *args, **kwargs)

    def info(self, msg, msgid=NILVALUE, structured_data=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        Args:
            msg:
                Message to log
            msgid:
                RFC 5424 MSGID
            structured_data:
                RFC 5424 STRUCTURED-DATA
        """
        if structured_data is None:
            structured_data = {}
        self._update(msgid, structured_data, kwargs)
        super(Rfc5424SysLogLogger, self).info(msg, *args, **kwargs)

    def warning(self, msg, msgid=NILVALUE, structured_data=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        Args:
            msg:
                Message to log
            msgid:
                RFC 5424 MSGID
            structured_data:
                RFC 5424 STRUCTURED-DATA
        """
        if structured_data is None:
            structured_data = {}
        self._update(msgid, structured_data, kwargs)
        super(Rfc5424SysLogLogger, self).warning(msg, *args, **kwargs)

    def error(self, msg, msgid=NILVALUE, structured_data=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        Args:
            msg:
                Message to log
            msgid:
                RFC 5424 MSGID
            structured_data:
                RFC 5424 STRUCTURED-DATA
        """
        if structured_data is None:
            structured_data = {}
        self._update(msgid, structured_data, kwargs)
        super(Rfc5424SysLogLogger, self).error(msg, *args, **kwargs)

    def critical(self, msg, msgid=NILVALUE, structured_data=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.

        Args:
            msg:
                Message to log
            msgid:
                RFC 5424 MSGID
            structured_data:
                RFC 5424 STRUCTURED-DATA
        """
        if structured_data is None:
            structured_data = {}
        self._update(msgid, structured_data, kwargs)
        super(Rfc5424SysLogLogger, self).critical(msg, *args, **kwargs)

    def log(self, level, msg, msgid=NILVALUE, structured_data=None, *args, **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.

        Args:
            level:
                Severity level as an integer
            msg:
                Message to log
            msgid:
                RFC 5424 MSGID
            structured_data:
                RFC 5424 STRUCTURED-DATA
        """
        if structured_data is None:
            structured_data = {}
        self._update(msgid, structured_data, kwargs)
        super(Rfc5424SysLogLogger, self).log(level, msg, *args, **kwargs)

    @staticmethod
    def _update(msgid, structured_data, kwargs):
        extra = dict(msgid=msgid, structured_data=structured_data)
        if 'extra' not in kwargs or not isinstance(kwargs['extra'], dict):
            kwargs['extra'] = dict()
        kwargs['extra'].update(extra)
