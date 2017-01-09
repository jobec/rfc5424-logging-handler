import logging
from rfc5424logging import Rfc5424SysLogHandler
import socket

logger = logging.getLogger('test.test')
logger.addHandler(Rfc5424SysLogHandler(address=('10.107.106.4', 5013)))
logger.setLevel(logging.DEBUG)

extra = {
    'structured_data': {
        'aaa': {'a': "A\u0394"}
    }
}

logger.info("ccc\u0394ccc\nddd", extra=extra)
logger.info("xxx\u0394xxx", extra=extra)
logger.error("e"*4000+'s')
