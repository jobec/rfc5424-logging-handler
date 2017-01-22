# coding=utf-8
from mock import patch

from conftest import address, message
from rfc5424logging import Rfc5424SysLogHandler


def test_unicode_msg(logger_with_udp_handler):
    expected_msg = (b'<10>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is a \xce\x94 message')
    logger, syslog_socket = logger_with_udp_handler
    logger.critical(u'This is a Δ message')
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_unicode_sd(logger_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id@32473 my_key="my_\xce\x94_value"] \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    logger.info(message,
                extra={'structured_data': {'my_sd_id@32473': {'my_key': u'my_Δ_value'}}})
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_unicode_hostname(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 my?machine root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, hostname=u'myΔmachine')
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        logger.info(message)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_unicode_appname(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname my?app 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, appname=u'myΔapp')
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        logger.info(message)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_unicode_msgid(adapter_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' my?msgid - \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.info(message, msgid=u'myΔmsgid')
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)
