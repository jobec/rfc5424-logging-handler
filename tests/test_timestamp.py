# coding=utf-8
import logging

import pytest
from conftest import (
    address, message
)
from mock import patch

from rfc5424logging import Rfc5424SysLogHandler


@pytest.mark.parametrize("handler_kwargs,expected", [
    (
        {'address': address, "utc_timestamp": True},
        b'<14>1 2000-01-01T11:11:11.111111+00:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ), (
        {'address': address,},
        b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
        b' - - \xef\xbb\xbfThis is an interesting message'
    ),
])
def test_timestamp(logger, handler_kwargs, expected):
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
