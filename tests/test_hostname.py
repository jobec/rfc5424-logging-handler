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
        {'address': address, 'hostname': ''},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'hostname': NILVALUE},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 - root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'hostname': None},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'hostname': 'my-hostname'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 my-hostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'hostname': 'my-loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'
                                         'oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'
                                         'oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'
                                         'ooooooooooooooooooooooooong-hostname'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 my-looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'
        b'oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'
        b'oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'hostname': 1234},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 1234 root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'hostname': 'my_Δhost \nname'},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 my_hostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address, 'hostname': SomeClass()},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 MyClassObject root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ),
])
def test_hostname(logger, handler_kwargs, expected):
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
