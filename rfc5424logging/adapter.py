import logging
from .handler import NOTICE, EMERGENCY, ALERT


class Rfc5424SysLogAdapter(logging.LoggerAdapter):
    _extra_levels_enabled = False

    def __init__(self, logger, extra=None, enable_extra_levels=False):
        """
        Initialize the adapter with a logger and a dict-like object which
        provides contextual information. This constructor signature allows
        easy stacking of LoggerAdapters, if so desired.

        You can effectively pass keyword arguments as shown in the
        following example:

        adapter = Rfc5424SysLogAdapter(someLogger, dict(p1=v1, p2="v2"))

        Args:
            logger:
                A Logger class instance
            enable_extra_levels (bool):
                Add custom log levels to the logging framework.
                Use with caution because it can conflict with other packages defining custom levels.
        """
        if enable_extra_levels and not Rfc5424SysLogAdapter._extra_levels_enabled:
            logging.addLevelName(EMERGENCY, 'EMERG')
            logging.addLevelName(EMERGENCY, 'EMERGENCY')
            logging.addLevelName(ALERT, 'ALERT')
            logging.addLevelName(NOTICE, 'NOTICE')
            Rfc5424SysLogAdapter._extra_levels_enabled = True

        super(Rfc5424SysLogAdapter, self).__init__(logger, extra or {})

    def process(self, msg, kwargs):
        """
        Searches for `msgid` and `sd` or `structured_data` in the keyword arguments
        and puts them in the `extra` keyword argument

        We don't touch other keyword arguments so we don't interfere with possible
        other logger adapters
        """
        hostname = kwargs.pop('hostname', None)
        appname = kwargs.pop('appname', None)
        procid = kwargs.pop('procid', None)
        msgid = kwargs.pop('msgid', None)
        structured_data = kwargs.pop('sd', None)

        if structured_data is None:
            structured_data = kwargs.pop('structured_data', None)

        if 'extra' not in kwargs:
            kwargs['extra'] = {}

        if hostname:
            kwargs['extra']['hostname'] = hostname
        if appname:
            kwargs['extra']['appname'] = appname
        if procid:
            kwargs['extra']['procid'] = procid
        if msgid:
            kwargs['extra']['msgid'] = msgid
        if structured_data:
            kwargs['extra']['structured_data'] = structured_data

        return msg, kwargs

    def log(self, level, msg, *args, **kwargs):
        # If custom levels are not enabled, we convert
        # the level to a standard one
        if not Rfc5424SysLogAdapter._extra_levels_enabled:
            if level == EMERGENCY or level == ALERT:
                level = logging.CRITICAL
            elif level == NOTICE:
                level = logging.WARNING
        super(Rfc5424SysLogAdapter, self).log(level, msg, *args, **kwargs)

    def emergency(self, msg, *args, **kwargs):
        self.log(EMERGENCY, msg, *args, **kwargs)
    emerg = emergency

    def alert(self, msg, *args, **kwargs):
        self.log(ALERT, msg, *args, **kwargs)

    def notice(self, msg, *args, **kwargs):
        self.log(NOTICE, msg, *args, **kwargs)
