from mock import patch

from conftest import address, message
from rfc5424logging import Rfc5424SysLogHandler


def test_long_hostname(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 my_hostnamemy_hostnamemy_hostnamemy_hostname'
                    b'my_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostname'
                    b'my_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostnamemy_hostname'
                    b'my_hostnamemy_hostnamemy_hostnamemy root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, hostname='my_hostname'*50)
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        logger.info(message)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_long_appname(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname '
                    b'my_loooooooooooooooooooooooooooooooooooooooooooo 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, appname='my_loooooooooooooooooooooooooooooooooooooooooooong_appname')
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        logger.info(message)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_long_procid(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root '
                    b'1234123412341234123412341234123412341234123412341234123412341234'
                    b'1234123412341234123412341234123412341234123412341234123412341234'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, procid="1234"*33)
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        logger.info(message)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_long_msgid(logger_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' SUPER_LOOOOOOOOOOOOOOOOOOOOOOONG - \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    logger.info(message, extra={'msgid': "SUPER_LOOOOOOOOOOOOOOOOOOOOOOONG_ID"})
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_long_sd_id(logger_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_loooooooooooooooooooooooooong my_key="my_value"] \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    logger.info(message,
                extra={'structured_data': {'my_loooooooooooooooooooooooooong_sd_id@32473': {'my_key': 'my_value'}}})
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_long_sd_key(logger_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id@32473 my_loooooooooooooooooooooooooong="my_value"] \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    logger.info(message,
                extra={'structured_data': {'my_sd_id@32473': {'my_loooooooooooooooooooooooooong_key': 'my_value'}}})
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)
