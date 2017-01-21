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
    def test_double_sd(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@32473 my_key="my_value"][my_sd_id2@32473 my_key2="my_value2"]'
                        b' \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info(
                'This is an %s message',
                msg_type,
                extra={'structured_data': OrderedDict([
                    ('my_sd_id@32473', {'my_key': 'my_value'}),
                    ('my_sd_id2@32473', {'my_key2': 'my_value2'})
                ])}
            )
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_multi_value(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@32473 my_key="my_value" my_key2="my_value2"]'
                        b' \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info(
                'This is an %s message',
                msg_type,
                extra={'structured_data': {
                    'my_sd_id@32473': OrderedDict([
                        ('my_key', 'my_value'),
                        ('my_key2', 'my_value2')
                    ])
                }}
            )
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_sd_with_init_pen(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@32473 my_key="my_value"] \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, enterprise_id=32473)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info(
                'This is an %s message',
                msg_type,
                extra={'structured_data': {'my_sd_id': {'my_key': 'my_value'}}}
            )
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_init_sd(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@ my_key="my_value"] \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sd = {'my_sd_id': {'my_key': 'my_value'}}
        sh = Rfc5424SysLogHandler(address=address, structured_data=sd)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_init_sd_and_msg_sd(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@ my_key="my_value"][my_sd_id2@ my_key2="my_value2"]'
                        b' \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sd = {'my_sd_id': {'my_key': 'my_value'}}
        sh = Rfc5424SysLogHandler(address=address, structured_data=sd)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info(
                'This is an %s message',
                msg_type,
                extra={'structured_data': {'my_sd_id2': {'my_key2': 'my_value2'}}}
            )
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_init_sd_and_msg_sd_with_init_pen(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@32473 my_key="my_value"][my_sd_id2@32473 my_key2="my_value2"]'
                        b' \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sd = {'my_sd_id': {'my_key': 'my_value'}}
        sh = Rfc5424SysLogHandler(address=address, structured_data=sd, enterprise_id=32473)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info(
                'This is an %s message',
                msg_type,
                extra={'structured_data': {'my_sd_id2': {'my_key2': 'my_value2'}}}
            )
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_empty_sd(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@32473] \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.INFO)
        sh = Rfc5424SysLogHandler(address=address, enterprise_id=32473)
        logger.addHandler(sh)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            logger.info(
                'This is an %s message',
                msg_type,
                extra={'structured_data': {'my_sd_id': None}}
            )
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)
