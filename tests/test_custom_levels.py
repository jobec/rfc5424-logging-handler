from conftest import address, message
from rfc5424logging import Rfc5424SysLogAdapter, NOTICE


def test_log(logger_with_udp_handler):
    expected_msg = (b'<13>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    adapter = Rfc5424SysLogAdapter(logger, enable_extra_levels=True)
    adapter.log(NOTICE, message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_log_not_enabled(adapter_with_udp_handler):
    expected_msg = (b'<12>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.log(NOTICE, message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_emergency(logger_with_udp_handler):
    expected_msg = (b'<8>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    adapter = Rfc5424SysLogAdapter(logger, enable_extra_levels=True)
    adapter.emerg(message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_emergency_not_enabled(adapter_with_udp_handler):
    expected_msg = (b'<10>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.emergency(message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_alert(logger_with_udp_handler):
    expected_msg = (b'<9>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    adapter = Rfc5424SysLogAdapter(logger, enable_extra_levels=True)
    adapter.alert(message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_alert_not_enabled(adapter_with_udp_handler):
    expected_msg = (b'<10>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.alert(message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_notice(logger_with_udp_handler):
    expected_msg = (b'<13>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    adapter = Rfc5424SysLogAdapter(logger, enable_extra_levels=True)
    adapter.notice(message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_notice_not_enabled(adapter_with_udp_handler):
    expected_msg = (b'<12>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.notice(message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)
