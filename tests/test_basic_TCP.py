from mock import patch
import logging
from rfc5424logging import Rfc5424SysLogHandler
from collections import OrderedDict
import pytz
import socket

address = ('127.0.0.1', 514)
timezone = pytz.timezone('Antarctica/Vostok')


def connect_mock(param1):
    return


@patch('logging.os.getpid', return_value=111)
@patch('logging.time.time', return_value=946725071.111111)
@patch('rfc5424logging.handler.get_localzone', return_value=timezone)
@patch('rfc5424logging.handler.socket.gethostname', return_value="testhostname")
@patch('logging.handlers.socket.socket.connect', side_effect=connect_mock)
@patch('logging.handlers.socket.socket.sendall', side_effect=connect_mock)
class TestRfc5424:
    def test_basic(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbfThis is an interesting message\n')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address, socktype=socket.SOCK_STREAM)
        logger.addHandler(sh)
        with patch.object(sh, 'socket', side_effect=connect_mock) as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendall.assert_called_with(expected_msg)
        logger.removeHandler(sh)

    def test_hostname(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 my_hostname syslogtest 111'
                        b' - - \xef\xbb\xbfThis is an interesting message\n')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, hostname='my_hostname', socktype=socket.SOCK_STREAM)
        logger.addHandler(sh)
        with patch.object(sh, 'socket', side_effect=connect_mock) as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendall.assert_called_with(expected_msg)
        logger.removeHandler(sh)

    def test_appname(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname my_appname 111'
                        b' - - \xef\xbb\xbfThis is an interesting message\n')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, appname='my_appname', socktype=socket.SOCK_STREAM)
        logger.addHandler(sh)
        with patch.object(sh, 'socket', side_effect=connect_mock) as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendall.assert_called_with(expected_msg)
        logger.removeHandler(sh)

    def test_procid(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 1234'
                        b' - - \xef\xbb\xbfThis is an interesting message\n')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, procid=1234, socktype=socket.SOCK_STREAM)
        logger.addHandler(sh)
        with patch.object(sh, 'socket', side_effect=connect_mock) as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendall.assert_called_with(expected_msg)
        logger.removeHandler(sh)

    def test_msgid(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' SUPER_DUPER_ID - \xef\xbb\xbfThis is an interesting message\n')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, socktype=socket.SOCK_STREAM)
        logger.addHandler(sh)
        with patch.object(sh, 'socket', side_effect=connect_mock) as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type, extra={'msgid': "SUPER_DUPER_ID"})
            syslog_socket.sendall.assert_called_with(expected_msg)
        logger.removeHandler(sh)

    def test_sd(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@32473 my_key="my_value"] \xef\xbb\xbfThis is an interesting message\n')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, socktype=socket.SOCK_STREAM)
        logger.addHandler(sh)
        with patch.object(sh, 'socket', side_effect=connect_mock) as syslog_socket:
            msg_type = 'interesting'
            logger.info(
                'This is an %s message',
                msg_type,
                extra={'structured_data': {'my_sd_id@32473': {'my_key': 'my_value'}}}
            )
            syslog_socket.sendall.assert_called_with(expected_msg)
        logger.removeHandler(sh)

    def test_framing_octet_counting(self, *args):
        expected_msg = (b'104 <14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address,
                                  socktype=socket.SOCK_STREAM,
                                  framing=Rfc5424SysLogHandler.FRAMING_OCTET_COUNTING)
        logger.addHandler(sh)
        with patch.object(sh, 'socket', side_effect=connect_mock) as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendall.assert_called_with(expected_msg)
        logger.removeHandler(sh)
