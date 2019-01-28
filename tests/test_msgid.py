# coding=utf-8
import logging

import pytest
from conftest import (
    address, message, SomeClass
)
from mock import patch

from rfc5424logging import Rfc5424SysLogHandler, NILVALUE


@pytest.mark.parametrize("logger_kwargs,expected", [
    (
        {},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'extra': {'msgid': ''}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'extra': {'msgid': None}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'extra': {'msgid': NILVALUE}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'extra': {'msgid': 'my_msgid'}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' my_msgid - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'extra': {'msgid': 'my_loooooooooooooooooooooooooong_msgid'}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' my_loooooooooooooooooooooooooong - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'extra': {'msgid': 1234}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' 1234 - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'extra': {'msgid': 'my_Δmsg \nid'}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' my_msgid - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'extra': {'msgid': SomeClass()}},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' MyClassObject - \xef\xbb\xbfThis is an interesting message'
    ),
])
def test_msgid(logger, logger_kwargs, expected):
    sh = Rfc5424SysLogHandler(address=address)
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
