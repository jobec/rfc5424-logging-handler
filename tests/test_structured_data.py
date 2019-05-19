# coding=utf-8
import logging

from conftest import (
    address, message, sd1, sd2, sd_multi_param, sd_multi_id, sd1_no_pen,
    sd_multi_param_no_pen, sd1_param_none_value, sd1_param_object_value,
    sd1_param_none_key
)
from mock import patch
import pytest

from rfc5424logging import Rfc5424SysLogHandler


@pytest.mark.parametrize("handler_kwargs,logger_kwargs,expected", [
    (     # 0
        {'address': address},
        {'extra': {'structured_data': sd1}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 1
        {'address': address, 'structured_data': sd1},
        {},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 2
        {'address': address, 'structured_data': sd1},
        {'extra': {'structured_data': sd2}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_value1"][my_sd_id2@32473 my_key2="my_value2"]'
        b' \xef\xbb\xbfThis is an interesting message'
    ), (  # 3
        {'address': address, 'structured_data': sd1},
        {'extra': {'structured_data': sd1}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 4
        {'address': address},
        {'extra': {'structured_data': sd_multi_id}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_value1"][my_sd_id2@32473 my_key2="my_value2"]'
        b' \xef\xbb\xbfThis is an interesting message'
    ), (  # 5
        {'address': address},
        {'extra': {'structured_data': sd_multi_param}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_value1" my_key2="my_value2"]'
        b' \xef\xbb\xbfThis is an interesting message'
    ), (  # 6
        {'address': address, 'enterprise_id': 32473},
        {'extra': {'structured_data': sd1_no_pen}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 7
        {'address': address},
        {'extra': {'structured_data': None}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (  # 8
        {'address': address, 'structured_data': None},
        {},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (  # 9
        {'address': address},
        {'extra': {'structured_data': 'just a string'}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (  # 10
        {'address': address},
        {'extra': {'structured_data': sd1_param_none_value}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1=""] \xef\xbb\xbfThis is an interesting message'
    ), (  # 11
        {'address': address},
        {'extra': {'structured_data': sd1_param_object_value}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="MyClass Object"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 12
        {'address': address},
        {'extra': {'structured_data': sd1_param_none_key}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 None="my_value1"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 13
        {'address': address},
        {'extra': {'structured_data': {'my_sd_id1@32473': {'my_= ]"Δkey1': 'my_value1'}}}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 14
        {'address': address},
        {'extra': {'structured_data': {'my_sd_id1@32473': {'my_key1': 'my]_\\value"\n1'}}}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my\\]_\\\\value\\"\n1"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 15
        {'address': address},
        {'extra': {'structured_data': {'my_sd_id1@32473': None}}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473] \xef\xbb\xbfThis is an interesting message'
    ), (  # 16
        {'address': address},
        {'extra': {'structured_data': {'my_=sd _id ]\n\r"Δ1@32473': {'my_key1': 'my_value1'}}}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 17
        {'address': address},
        {'extra': {'structured_data': {'my_@sd_id1@32473': {'my_key1': 'my_value1'}}}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 18
        {'address': address},
        {'extra': {'structured_data': {'my_sd_id1@32473': {'my_key1': 'my_Δ_value1'}}}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473 my_key1="my_\xce\x94_value1"] \xef\xbb\xbfThis is an interesting message'
    ), (  # 19
        {'address': address},
        {'extra': {'structured_data': {'my_sddddddddddddddddddddddddddddddddd_ID@32473': {'my_key1': 'my_value1'}}}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sdddddddddddddddddddddd@32473 my_key1="my_value1"] '
        b'\xef\xbb\xbfThis is an interesting message'
    ), (  # 20
        {'address': address, 'enterprise_id': 32473},
        {'extra': {'structured_data': {'my_sddddddddddddddddddddddddddddddddd_ID': {'my_key1': 'my_value1'}}}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sdddddddddddddddddddddd@32473 my_key1="my_value1"]'
        b' \xef\xbb\xbfThis is an interesting message'
    ), (  # 21
        {'address': address, 'enterprise_id': 32473},
        {'extra': {'structured_data': {'timeQuality': {'isSynced': '1'}}}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [timeQuality isSynced="1"]'
        b' \xef\xbb\xbfThis is an interesting message'
    ), (  # 22
        {'address': address, 'enterprise_id': "32473.1.2"},
        {'extra': {'structured_data': sd1_no_pen}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - [my_sd_id1@32473.1.2 my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message'
    ),
])
def test_sd(logger, handler_kwargs, logger_kwargs, expected):
    sh = Rfc5424SysLogHandler(**handler_kwargs)
    logger.addHandler(sh)
    with patch.object(sh.transport, 'socket') as syslog_socket:
        logger.info(message, **logger_kwargs)
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()

        logger.log(logging.INFO, message, **logger_kwargs)
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()

        logging.info(message, **logger_kwargs)
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()
    logger.removeHandler(sh)


@pytest.mark.parametrize("handler_kwargs,logger_kwargs", [
    (
        {'address': address},
        {'extra': {'structured_data': sd_multi_param_no_pen}},
    ), (
        {'address': address},
        {'extra': {'structured_data': {'my_sd_id@3247332473324733247332473324735': {'my_key1': 'my_value1'}}}},
    )
])
def test_sd_not_sent(logger, handler_kwargs, logger_kwargs):
    sh = Rfc5424SysLogHandler(**handler_kwargs)
    logger.addHandler(sh)
    with patch.object(sh.transport, 'socket') as syslog_socket:
        logger.info(message, **logger_kwargs)
        syslog_socket.sendto.assert_not_called()
    logger.removeHandler(sh)


def test_sd_in_message_with_adapter(adapter_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id1@32473 my_key1="my_value1"] \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.info(message, structured_data=sd1)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


