import logging

from mock import patch

from conftest import address, message
from rfc5424logging import Rfc5424SysLogHandler


def test_basic(logger_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    logger.info(message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_basic_from_logging(logger_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    logging.info(message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_log(logger_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    logger.log(logging.INFO, message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_msgid(logger_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' SUPER_DUPER_ID - \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    logger.info(message, extra={'msgid': "SUPER_DUPER_ID"})
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_sd(logger_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id@32473 my_key="my_value"] \xef\xbb\xbfThis is an interesting message')
    logger, syslog_socket = logger_with_udp_handler
    logger.info(message,
                extra={'structured_data': {'my_sd_id@32473': {'my_key': 'my_value'}}})
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_hostname(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 my_hostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, hostname='my_hostname')
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        logger.info(message)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_appname(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname my_appname 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, appname='my_appname')
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        logger.info(message)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_procid(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 1234'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, procid=1234)
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        logger.info(message)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_str_procid(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 1234'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, procid="1234")
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        logger.info(message)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)
