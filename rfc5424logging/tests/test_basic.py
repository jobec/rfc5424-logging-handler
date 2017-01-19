import logging
from sys import platform
from unittest import TestCase

from rfc5424logging import Rfc5424SysLogHandler, Rfc5424SysLogLogger

ADDRESS = '/var/run/syslog' if platform == 'darwin' else ('127.0.0.1', 514)


class TestRfc5424(TestCase):
    def test_basic(self):
        logger = Rfc5424SysLogLogger('syslogtest')
        logger.setLevel(logging.INFO)

        sh = Rfc5424SysLogHandler(ADDRESS)
        logger.addHandler(sh)
        msg_type = 'interesting'
        logger.info('This is an {} message'.format(msg_type))

    def test_basic_msgid(self):
        logger = Rfc5424SysLogLogger('syslogtest')
        logger.setLevel(logging.INFO)

        sh = Rfc5424SysLogHandler(ADDRESS)
        logger.addHandler(sh)
        msg_type = 'interesting'
        logger.debug('This is an {} message with a msgid'.format(msg_type), msgid='TCPIN')

    def test_basic_structured_data(self):
        logger = Rfc5424SysLogLogger('syslogtest')
        logger.setLevel(logging.INFO)

        sh = Rfc5424SysLogHandler(ADDRESS)
        logger.addHandler(sh)
        msg_type = 'interesting'
        structured_data = {
            "exampleSDID@32473 iut": "3",
            "eventSource": "Application",
            "eventID": "1011"
        }
        logger.warning('This is an {} message with structured_data'.format(msg_type), structured_data=structured_data)
