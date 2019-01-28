import logging
import socket
from collections import OrderedDict
from six import python_2_unicode_compatible
import pytest
import pytz
from mock import patch

from rfc5424logging import Rfc5424SysLogHandler, Rfc5424SysLogAdapter


class SomeClass:
    def __init__(self):
        self.a = "a"
        self.b = 1

    def __str__(self):
        return "MyClass Object"


address = ('127.0.0.1', 514)
timezone = pytz.timezone('Antarctica/Vostok')
message = 'This is an interesting message'

sd1 = {'my_sd_id1@32473': {'my_key1': 'my_value1'}}
sd2 = {'my_sd_id2@32473': {'my_key2': 'my_value2'}}
sd_multi_id = OrderedDict()
sd_multi_id.update(sd1)
sd_multi_id.update(sd2)
sd_multi_param = {'my_sd_id1@32473': OrderedDict([('my_key1', 'my_value1'), ('my_key2', 'my_value2')])}

sd1_no_pen = {'my_sd_id1': {'my_key1': 'my_value1'}}
sd2_no_pen = {'my_sd_id2': {'my_key2': 'my_value2'}}
sd_multi_id_no_pen = OrderedDict()
sd_multi_id_no_pen.update(sd1_no_pen)
sd_multi_id_no_pen.update(sd2_no_pen)
sd_multi_param_no_pen = {'my_sd_id1': OrderedDict([('my_key1', 'my_value1'), ('my_key2', 'my_value2')])}

sd1_param_none_value = {'my_sd_id1@32473': {'my_key1': None}}
sd1_param_object_value = {'my_sd_id1@32473': {'my_key1': SomeClass()}}
sd1_param_none_key = {'my_sd_id1@32473': {None: 'my_value1'}}


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

    logging.raiseExceptions = True
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
    with patch.object(sh.transport, 'socket') as syslog_socket:
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
    with patch.object(sh.transport, 'socket', side_effect=connect_mock) as syslog_socket:
        yield logger, syslog_socket
    logger.removeHandler(sh)
