# coding=utf-8
import logging
import socket

from conftest import (
    address, message, connect_mock, SomeClass
)
from mock import patch
import pytest
from rfc5424logging import Rfc5424SysLogHandler, NILVALUE


@pytest.mark.parametrize("handler_kwargs,expected", [
    (
        {'address': address},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'procid': ''},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'procid': None},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'procid': NILVALUE},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root -'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'procid': '1234'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 1234'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'procid': '1234123412341234123412341234123412341234123412341234123412341234123412341234'
                                       '1234123412341234123412341234123412341234123412341234aaa'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 123412341234123412341234123412341234123412341234'
        b'12341234123412341234123412341234123412341234123412341234123412341234123412341234'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'procid': 1234},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 1234'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'procid': '12 \nΔ34'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 1234'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'procid': SomeClass()},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root MyClassObject'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ),
])
def test_procid(logger, handler_kwargs, expected):
    sh = Rfc5424SysLogHandler(**handler_kwargs)
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        logger.info(message)
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()

        logger.log(logging.INFO, message)
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()

        logging.info(message)
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()
    logger.removeHandler(sh)


@pytest.mark.parametrize("handler_kwargs,expected", [
    (
        {'address': address, 'socktype': socket.SOCK_STREAM},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message\n'
    ),
    (
        {'address': address, 'procid': "1234", 'socktype': socket.SOCK_STREAM},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 1234'
        b' - - \xef\xbb\xbfThis is an interesting message\n'
    ),
    (
        {'address': address, 'procid': 1234, 'socktype': socket.SOCK_STREAM},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 1234'
        b' - - \xef\xbb\xbfThis is an interesting message\n'
    ),
    (
        {'address': address, 'procid': '12 \nΔ34', 'socktype': socket.SOCK_STREAM},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 1234'
        b' - - \xef\xbb\xbfThis is an interesting message\n'
    ),
    (
        {'address': address, 'procid': SomeClass(), 'socktype': socket.SOCK_STREAM},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root MyClassObject'
        b' - - \xef\xbb\xbfThis is an interesting message\n'
    ),
])
def test_procid_tcp(logger, handler_kwargs, expected):
    sh = Rfc5424SysLogHandler(**handler_kwargs)
    logger.addHandler(sh)
    with patch.object(sh, 'socket', side_effect=connect_mock) as syslog_socket:
        logger.info(message)
        syslog_socket.sendall.assert_called_once_with(expected)
        syslog_socket.sendall.reset_mock()

        logger.log(logging.INFO, message)
        syslog_socket.sendall.assert_called_once_with(expected)
        syslog_socket.sendall.reset_mock()

        logging.info(message)
        syslog_socket.sendall.assert_called_once_with(expected)
        syslog_socket.sendall.reset_mock()
    logger.removeHandler(sh)
