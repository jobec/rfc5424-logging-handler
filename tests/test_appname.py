# coding=utf-8
import logging

import pytest
from conftest import (
    address, message, SomeClass
)
from mock import patch

from rfc5424logging import Rfc5424SysLogHandler, NILVALUE


@pytest.mark.parametrize("handler_kwargs,expected", [
    (
        {'address': address},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': ''},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': NILVALUE},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname - 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': None},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': 'my_appname'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname my_appname 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': 'my_loooooooooooooooooooooooooooooooooooooooooong_appname'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname my_loooooooooooooooooooooooooooooooooooooooooong 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': 1234},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname 1234 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': 'my_Δapp \nname'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname my_appname 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': SomeClass()},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname MyClassObject 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ),
])
def test_appname(logger, handler_kwargs, expected):
    sh = Rfc5424SysLogHandler(**handler_kwargs)
    logger.addHandler(sh)
    with patch.object(sh.transport, 'socket') as syslog_socket:
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
        {'address': address},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': ''},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': NILVALUE},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname - 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': None},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': 'my_appname'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname my_appname 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': 'my_loooooooooooooooooooooooooooooooooooooooooong_appname'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname my_loooooooooooooooooooooooooooooooooooooooooong 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': 1234},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname 1234 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': 'my_Δapp \nname'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname my_appname 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'appname': SomeClass()},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname MyClassObject 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ),
])
def test_appname(logger, handler_kwargs, expected):
    sh = Rfc5424SysLogHandler(handler_kwargs["address"])
    logger.addHandler(sh)
    with patch.object(sh.transport, 'socket') as syslog_socket:
        logger.info(message, extra=handler_kwargs)
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()

        logger.log(logging.INFO, message, extra=handler_kwargs)
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()

        logging.info(message, extra=handler_kwargs)
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()
    logger.removeHandler(sh)
