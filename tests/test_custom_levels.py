from mock import patch
import logging
from rfc5424logging import Rfc5424SysLogHandler, Rfc5424SysLogAdapter, NOTICE
import pytz

address = ('127.0.0.1', 514)
timezone = pytz.timezone('Antarctica/Vostok')


@patch('logging.os.getpid', return_value=111)
@patch('logging.time.time', return_value=946725071.111111)
@patch('rfc5424logging.handler.get_localzone', return_value=timezone)
@patch('rfc5424logging.handler.socket.gethostname', return_value="testhostname")
class TestRfc5424:
    def test_log(self, *args):
        expected_msg = (b'<13>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbf[NOTICE] This is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        if '_levelNames' in logging.__dict__:
            # Python 2.7
            patcher1 = patch.dict(logging._levelNames)
            patcher1.start()
        else:
            # Python 3.x
            patcher1 = patch.dict(logging._levelToName)
            patcher2 = patch.dict(logging._nameToLevel)
            patcher1.start()
            patcher2.start()
        adapter = Rfc5424SysLogAdapter(logger, enable_extra_levels=True)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.log(NOTICE, 'This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        if '_levelNames' in logging.__dict__:
            # Python 2.7
            patcher1.stop()
        else:
            # Python 3.x
            patcher1.stop()
            patcher2.stop()
        logger.removeHandler(sh)
        Rfc5424SysLogAdapter._extra_levels_enabled = False

    def test_log_not_enabled(self, *args):
        expected_msg = (b'<12>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbf[WARNING] This is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        adapter = Rfc5424SysLogAdapter(logger)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.log(NOTICE, 'This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_emergency(self, *args):
        expected_msg = (b'<8>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbf[EMERGENCY] This is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        if '_levelNames' in logging.__dict__:
            # Python 2.7
            patcher1 = patch.dict(logging._levelNames)
            patcher1.start()
        else:
            # Python 3.x
            patcher1 = patch.dict(logging._levelToName)
            patcher2 = patch.dict(logging._nameToLevel)
            patcher1.start()
            patcher2.start()
        adapter = Rfc5424SysLogAdapter(logger, enable_extra_levels=True)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.emerg('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        if '_levelNames' in logging.__dict__:
            # Python 2.7
            patcher1.stop()
        else:
            # Python 3.x
            patcher1.stop()
            patcher2.stop()
        logger.removeHandler(sh)
        Rfc5424SysLogAdapter._extra_levels_enabled = False

    def test_emergency_not_enabled(self, *args):
        expected_msg = (b'<10>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbf[CRITICAL] This is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        adapter = Rfc5424SysLogAdapter(logger)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.emergency('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_alert(self, *args):
        expected_msg = (b'<9>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbf[ALERT] This is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        if '_levelNames' in logging.__dict__:
            # Python 2.7
            patcher1 = patch.dict(logging._levelNames)
            patcher1.start()
        else:
            # Python 3.x
            patcher1 = patch.dict(logging._levelToName)
            patcher2 = patch.dict(logging._nameToLevel)
            patcher1.start()
            patcher2.start()
        adapter = Rfc5424SysLogAdapter(logger, enable_extra_levels=True)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.alert('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        if '_levelNames' in logging.__dict__:
            # Python 2.7
            patcher1.stop()
        else:
            # Python 3.x
            patcher1.stop()
            patcher2.stop()
        logger.removeHandler(sh)
        Rfc5424SysLogAdapter._extra_levels_enabled = False

    def test_alert_not_enabled(self, *args):
        expected_msg = (b'<10>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbf[CRITICAL] This is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        adapter = Rfc5424SysLogAdapter(logger)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.alert('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)

    def test_notice(self, *args):
        expected_msg = (b'<13>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbf[NOTICE] This is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        if '_levelNames' in logging.__dict__:
            # Python 2.7
            patcher1 = patch.dict(logging._levelNames)
            patcher1.start()
        else:
            # Python 3.x
            patcher1 = patch.dict(logging._levelToName)
            patcher2 = patch.dict(logging._nameToLevel)
            patcher1.start()
            patcher2.start()
        adapter = Rfc5424SysLogAdapter(logger, enable_extra_levels=True)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.notice('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        if '_levelNames' in logging.__dict__:
            # Python 2.7
            patcher1.stop()
        else:
            # Python 3.x
            patcher1.stop()
            patcher2.stop()
        logger.removeHandler(sh)
        Rfc5424SysLogAdapter._extra_levels_enabled = False

    def test_notice_not_enabled(self, *args):
        expected_msg = (b'<12>1 2000-01-01T17:11:11.111111+06:00 testhostname syslogtest 111'
                        b' - - \xef\xbb\xbf[WARNING] This is an interesting message')
        logger = logging.getLogger('syslogtest')
        logger.setLevel(logging.DEBUG)
        sh = Rfc5424SysLogHandler(address=address)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        adapter = Rfc5424SysLogAdapter(logger)
        with patch.object(sh, 'socket') as syslog_socket:
            msg_type = 'interesting'
            adapter.notice('This is an %s message', msg_type)
            syslog_socket.sendto.assert_called_once_with(expected_msg, address)
        logger.removeHandler(sh)
