from mock import patch
import logging
from rfc5424logging import Rfc5424SysLogHandler, Rfc5424SysLogAdapter
import pytest
import pytz
import socket

address = ('127.0.0.1', 514)
timezone = pytz.timezone('Antarctica/Vostok')
message = 'This is an interesting message'

def connect_mock(param1):
    return


@pytest.fixture
def logger():
    getpid_patch = patch('logging.os.getpid', return_value=111)
    getpid_patch.start()
    time_patch = patch('logging.time.time', return_value=946725071.111111)
    time_patch.start()
    localzone_patch = patch('rfc5424logging.handler.get_localzone', return_value=timezone)
    localzone_patch.start()
    hostname_patch = patch('rfc5424logging.handler.socket.gethostname', return_value="testhostname")
    hostname_patch.start()
    connect_patch = patch('logging.handlers.socket.socket.connect', side_effect=connect_mock)
    connect_patch.start()
    sendall_patch = patch('logging.handlers.socket.socket.sendall', side_effect=connect_mock)
    sendall_patch.start()

    if '_levelNames' in logging.__dict__:
        # Python 2.7
        level_patch = patch.dict(logging._levelNames)
        level_patch.start()
    else:
        # Python 3.x
        level_patch1 = patch.dict(logging._levelToName)
        level_patch1.start()
        level_patch2 = patch.dict(logging._nameToLevel)
        level_patch2.start()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    yield logger

    getpid_patch.stop()
    time_patch.stop()
    localzone_patch.stop()
    hostname_patch.stop()
    connect_patch.stop()
    sendall_patch.stop()

    if '_levelNames' in logging.__dict__:
        # Python 2.7
        level_patch.stop()
    else:
        # Python 3.x
        level_patch1.stop()
        level_patch2.stop()

    Rfc5424SysLogAdapter._extra_levels_enabled = False


@pytest.fixture
def logger_with_udp_handler(logger):
    sh = Rfc5424SysLogHandler(address=address)
    logger.addHandler(sh)
    with patch.object(sh, 'socket') as syslog_socket:
        yield logger, syslog_socket
    logger.removeHandler(sh)


@pytest.fixture
def adapter_with_udp_handler(logger_with_udp_handler):
    logger, syslog_socket = logger_with_udp_handler
    adapter = Rfc5424SysLogAdapter(logger)
    yield adapter, syslog_socket


@pytest.fixture
def logger_with_tcp_handler(logger):
    sh = Rfc5424SysLogHandler(address=address, socktype=socket.SOCK_STREAM)
    logger.addHandler(sh)
    with patch.object(sh, 'socket', side_effect=connect_mock) as syslog_socket:
        yield logger, syslog_socket
    logger.removeHandler(sh)
