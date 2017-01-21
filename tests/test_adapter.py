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
    def test_info(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        adapter = Rfc5424SysLogAdapter(logger)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.info('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_log(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        adapter = Rfc5424SysLogAdapter(logger)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.log(logging.INFO, 'This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_msgid(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' SUPER_DUPER_ID - \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        adapter = Rfc5424SysLogAdapter(logger)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.info('This is an %s message', msg_type, msgid="SUPER_DUPER_ID")
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_sd(self, *args):
        expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - [my_sd_id@32473 my_key="my_value"] \xef\xbb\xbfThis is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        logger.addHandler(sh)
        adapter = Rfc5424SysLogAdapter(logger)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.info(
                'This is an %s message',
                msg_type,
                structured_data={'my_sd_id@32473': {'my_key': 'my_value'}}
            )
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)
