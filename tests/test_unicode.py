# coding=utf-8
from mock import patch
import logging
from rfc5424logging import Rfc5424SysLogHandler, Rfc5424SysLogAdapter
import pytz

address = ('127.0.0.1', 514)
timezone = pytz.timezone('Antarctica/Vostok')


@patch('logging.os.getpid', return_value=111)
@patch('logging.time.time', return_value=946725071.111111)
@patch('rfc5424logging.handler.get_localzone', return_value=timezone)
@patch('rfc5424logging.handler.socket.gethostname', return_value="testhostname")
class TestRfc5424:
    def test_unicode_msg(self, *args):
        expected_msg = (b'<10>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbfThis is a \xce\x94 message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            logger.critical(u'This is a Δ message')
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_unicode_sd(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@32473 my_key="my_\xce\x94_value"] \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info(
                'This is an %s message',
                msg_type,
                extra={'structured_data': {'my_sd_id@32473': {'my_key': u'my_Δ_value'}}}
            )
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_unicode_hostname(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 my?machine syslogtest 111'
                        b' - - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, hostname=u'myΔmachine')
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_unicode_appname(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname my?app 111'
                        b' - - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, appname=u'myΔapp')
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_unicode_msgid(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' my?msgid - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        adapter = Rfc5424SysLogAdapter(logger)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.info('This is an %s message', msg_type, msgid=u'myΔmsgid')
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)
