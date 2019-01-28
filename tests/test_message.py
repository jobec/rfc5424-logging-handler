# coding=utf-8
import logging

import pytest
from conftest import (
    address, message, SomeClass
)
from mock import patch

from rfc5424logging import Rfc5424SysLogHandler, NILVALUE


def test_unicode_msg(logger):
    sh = Rfc5424SysLogHandler(address=address)
    logger.addHandler(sh)
    message = u"This is a ℛℯα∂α♭ℓℯ message"
    with patch.object(sh.transport, 'socket') as syslog_socket:
        logger.info(message)
        expected = b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111' \
                   b' - - \xef\xbb\xbfThis is a \xe2\x84\x9b\xe2\x84\xaf\xce\xb1\xe2\x88\x82' \
                   b'\xce\xb1\xe2\x99\xad\xe2\x84\x93\xe2\x84\xaf message'
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()
    logger.removeHandler(sh)


def test_msg_any(logger):
    sh = Rfc5424SysLogHandler(address=address, msg_as_utf8=False)
    logger.addHandler(sh)
    with patch.object(sh.transport, 'socket') as syslog_socket:
        logger.info(message)
        expected = b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111' \
                   b' - - This is an interesting message'
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()
    logger.removeHandler(sh)


def test_empty_msg(logger):
    sh = Rfc5424SysLogHandler(address=address, msg_as_utf8=False)
    logger.addHandler(sh)
    with patch.object(sh.transport, 'socket') as syslog_socket:
        logger.info(None)
        expected = b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111 - -'
        syslog_socket.sendto.assert_called_once_with(expected, address)
        syslog_socket.sendto.reset_mock()
    logger.removeHandler(sh)
