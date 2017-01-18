from unittest import TestCase
import logging
from rfc5424logging import Rfc5424SysLogHandler


class TestRfc5424(TestCase):
    def test_basic(self):

        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)

        sh = Rfc5424SysLogHandler(address=('127.0.0.1', 514))
        logger.addHandler(sh)
        msg_type = 'interesting'
        logger.info('This is an %s message', msg_type)

