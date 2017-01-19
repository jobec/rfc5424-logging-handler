import logging


class Rfc5424SysLogAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super(Rfc5424SysLogAdapter, self).__init__(logger, extra or {})

    def process(self, msg, kwargs):
        return msg, kwargs

    def log(self, level, msg, *args, **kwargs):
        msgid = kwargs.pop('msgid', None)
        structured_data = kwargs.pop('structured_data', None)

        if 'extra' not in kwargs:
            kwargs['extra'] = {}

        if msgid:
            kwargs['extra']['msgid'] = msgid
        if structured_data:
            kwargs['extra']['structured_data'] = structured_data

        super(Rfc5424SysLogAdapter, self).log(level, msg, *args, **kwargs)
