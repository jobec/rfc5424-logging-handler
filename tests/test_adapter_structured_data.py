import logging
from collections import OrderedDict

from mock import patch

from conftest import address, message
from rfc5424logging import Rfc5424SysLogHandler, Rfc5424SysLogAdapter

sd1 = {'my_sd_id1': {'my_key1': 'my_value1'}}
sd2 = {'my_sd_id2': {'my_key2': 'my_value2'}}
sd_double = OrderedDict()
sd_double.update(sd1)
sd_double.update(sd2)


def test_log(adapter_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id1@ my_key1="my_value1"][my_sd_id2@ my_key2="my_value2"]'
                    b' \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.log(logging.INFO, message, structured_data=sd_double)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_alternate_sd(adapter_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id1@ my_key1="my_value1"][my_sd_id2@ my_key2="my_value2"]'
                    b' \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.info(message, sd=sd_double)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_sd_with_init_pen(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id1@32473 my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, enterprise_id=32473)
    logger.addHandler(sh)
    adapter = Rfc5424SysLogAdapter(logger)
    with patch.object(sh, 'socket') as syslog_socket:
        adapter.info(message, structured_data=sd1)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_init_sd(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id1@ my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, structured_data=sd1)
    logger.addHandler(sh)
    adapter = Rfc5424SysLogAdapter(logger)
    with patch.object(sh, 'socket') as syslog_socket:
        adapter.info(message)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_init_sd_and_msg_sd(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id1@ my_key1="my_value1"][my_sd_id2@ my_key2="my_value2"]'
                    b' \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, structured_data=sd1)
    logger.addHandler(sh)
    adapter = Rfc5424SysLogAdapter(logger)
    with patch.object(sh, 'socket') as syslog_socket:
        adapter.info(message, structured_data=sd2)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_init_sd_and_msg_sd_with_init_pen(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id1@32473 my_key1="my_value1"][my_sd_id2@32473 my_key2="my_value2"]'
                    b' \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, structured_data=sd1, enterprise_id=32473)
    logger.addHandler(sh)
    adapter = Rfc5424SysLogAdapter(logger)
    with patch.object(sh, 'socket') as syslog_socket:
        adapter.info(message, structured_data=sd2)
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)


def test_empty_sd(logger):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id@32473] \xef\xbb\xbfThis is an interesting message')
    sh = Rfc5424SysLogHandler(address=address, enterprise_id=32473)
    logger.addHandler(sh)
    adapter = Rfc5424SysLogAdapter(logger)
    with patch.object(sh, 'socket') as syslog_socket:
        adapter.info(message, extra={'structured_data': {'my_sd_id': None}})
        syslog_socket.sendto.assert_called_once_with(expected_msg, address)
    logger.removeHandler(sh)
