from mock import patch
import logging
from rfc5424logging import Rfc5424SysLogHandler
from collections import OrderedDict
import pytz

address = ('127.0.0.1', 514)
timezone = pytz.timezone('Antarctica/Vostok')


@patch('logging.os.getpid', return_value=111)
@patch('logging.time.time', return_value=946725071.111111)
@patch('rfc5424logging.handler.get_localzone', return_value=timezone)
@patch('rfc5424logging.handler.socket.gethostname', return_value="testhostname")
class TestRfc5424:
    def test_long_hostname(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 my_hostnamemy_hostnamemy_hostnamemy_hostname'
                        b'my_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostname'
                        b'my_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostname'
                        b'my_hostnamemy_hostnamemy_hostnamemy syslogtest 111'
                        b' - - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, hostname='my_hostname'*50)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_long_appname(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname '
                        b'my_loooooooooooooooooooooooooooooooooooooooooooo 111'
                        b' - - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, appname='my_loooooooooooooooooooooooooooooooooooooooooooong_appname')
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_long_procid(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest '
                        b'1234123412341234123412341234123412341234123412341234123412341234'
                        b'1234123412341234123412341234123412341234123412341234123412341234'
                        b' - - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, procid="1234"*33)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_long_msgid(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' SUPER_LOOOOOOOOOOOOOOOOOOOOOOONG - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type, extra={'msgid': "SUPER_LOOOOOOOOOOOOOOOOOOOOOOONG_ID"})
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_long_sd_id(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_loooooooooooooooooooooooooong my_key="my_value"] \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info(
                'This is an %s message',
                msg_type,
                extra={'structured_data': {'my_loooooooooooooooooooooooooong_sd_id@32473': {'my_key': 'my_value'}}}
            )
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_long_sd_key(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@32473 my_loooooooooooooooooooooooooong="my_value"] \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info(
                'This is an %s message',
                msg_type,
                extra={'structured_data': {'my_sd_id@32473': {'my_loooooooooooooooooooooooooong_key': 'my_value'}}}
            )
            syslog_socket.sendto.assert_called_with(expected_msg, address)
        logger.removeHandler(sh)
