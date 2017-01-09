import datetime
import socket
import os
import sys
from logging.handlers import SysLogHandler, SYSLOG_UDP_PORT
from tzlocal import get_localzone
from collections import OrderedDict
from codecs import BOM_UTF8
import datetime

NILVALUE = '-'

SP = b' '
# As defined in RFC5424 Section 7
REGISTERED_SD_IDs = ('timeQuality', 'origin', 'meta')
# Version of the protocol we support
SYSLOG_VERSION = '1'

FRAMING_OCTET_COUNTING = 1
FRAMING_NON_TRANSPARENT = 2


class Rfc5424SysLogHandler(SysLogHandler, object):
    """An RFC 5424-complaint Syslog Handler for the python logging framework"""

    def __init__(self, address=('localhost', SYSLOG_UDP_PORT),
                 facility=SysLogHandler.LOG_USER,
                 socktype=socket.SOCK_DGRAM,
                 framing=FRAMING_NON_TRANSPARENT,
                 hostname=None, appname=None, procid=None, structured_data=None, enterprise_id=None):

        self.hostname = hostname
        self.appname = appname
        self.procid = procid
        self.structured_data = structured_data
        self.enterprise_id = enterprise_id
        self.framing = framing

        if self.hostname is None:
            self.hostname = socket.gethostname()
        if self.structured_data is None:
            self.structured_data = OrderedDict()

        super().__init__(address, facility, socktype)

    def get_hostname(self, record):
        return getattr(record, 'hostname', self.hostname)

    def get_appname(self, record):
        if self.appname is not None:
            return self.appname
        else:
            return getattr(record, 'name', NILVALUE)

    def get_procid(self, record):
        if self.procid is not None:
            return str(self.procid)
        else:
            return str(getattr(record, 'process', NILVALUE))

    def get_msgid(self, record):
        return getattr(record, 'msgid', NILVALUE)

    def get_enterprise_id(self, record):
        ent_id = getattr(record, 'enterprise_id', self.enterprise_id)
        if ent_id is None:
            ent_id = ''
        return ent_id

    def get_structured_data(self, record):
        structured_data = OrderedDict()
        structured_data.update(self.structured_data)
        structured_data.update(getattr(record, 'structured_data', {}))
        return structured_data

    def emit(self, record):
        """
        Emit a record.

        The record is formatted, and then sent to the syslog server. If
        exception information is present, it is NOT sent to the server.
        """

        # HEADER
        pri = '<%d>' % self.encodePriority(self.facility,
                                           self.mapPriority(record.levelname))
        version = SYSLOG_VERSION
        timestamp = datetime.datetime.fromtimestamp(record.created, get_localzone()).isoformat()
        hostname = self.get_hostname(record)
        appname = self.get_appname(record)
        procid = self.get_procid(record)
        msgid = self.get_msgid(record)

        pri = pri.encode('ascii')
        version = version.encode('ascii')
        timestamp = timestamp.encode('ascii')
        hostname = hostname.encode('ascii', 'replace')[:255]
        appname = appname.encode('ascii', 'replace')[:48]
        procid = procid.encode('ascii', 'replace')[:128]
        msgid = msgid.encode('ascii', 'replace')[:32]

        header = b''.join((pri, version, SP, timestamp, SP, hostname, SP, appname, SP, procid, SP, msgid))

        # STRUCTURED-DATA
        enterprise_id = self.get_enterprise_id(record)
        structured_data = self.get_structured_data(record)
        cleaned_structured_data = []
        for sd_id, sd_params in list(structured_data.items()):
            cleaned_sd_params = []
            # ignore sd params not int key-value format
            if isinstance(sd_params, dict):
                sd_params = sd_params.items()
            else:
                sd_params = []

            for (param_name, param_value) in sd_params:
                param_name = param_name.replace('=', '').replace(' ', '').replace(']', '').replace('"', '')
                param_value = param_value.replace('\\', '\\\\').replace('"', '\\"').replace(']', '\\]')

                param_name = param_name.encode('ascii', 'replace')[:32]
                param_value = param_value.encode('utf-8')

                sd_param = b''.join((param_name, b'="', param_value, b'"'))
                cleaned_sd_params.append(sd_param)

            cleaned_sd_params = SP.join(cleaned_sd_params)

            sd_id = sd_id.replace('=', '').replace(' ', '').replace(']', '').replace('"', '')
            if '@' not in sd_id and sd_id not in REGISTERED_SD_IDs:
                sd_id = '@'.join((sd_id, enterprise_id))
            sd_id = sd_id.encode('ascii', 'replace')[:32]

            sd_element = b''.join((b'[', sd_id, SP, cleaned_sd_params, b']'))
            cleaned_structured_data.append(sd_element)

        if cleaned_structured_data:
            structured_data = b''.join(cleaned_structured_data)
        else:
            structured_data = NILVALUE.encode('ascii')

        # MSG
        msg = self.format(record)
        msg = b''.join((BOM_UTF8, msg.encode('utf-8')))

        # SYSLOG-MSG
        # with RFC6587 framing
        if self.socktype == socket.SOCK_STREAM:
            if self.framing == FRAMING_NON_TRANSPARENT:
                msg = msg.replace(b'\n', b'\\n')
                syslog_msg = SP.join((header, structured_data, msg, b'\n'))
            else:
                syslog_msg = SP.join((header, structured_data, msg))
                syslog_msg = SP.join((str(len(syslog_msg)).encode('ascii'), syslog_msg))
        else:
            syslog_msg = SP.join((header, structured_data, msg))

        # Off it goes
        try:
            if self.unixsocket:
                try:
                    self.socket.send(syslog_msg)
                except OSError:
                    self.socket.close()
                    self._connect_unixsocket(self.address)
                    self.socket.send(syslog_msg)
            elif self.socktype == socket.SOCK_DGRAM:
                self.socket.sendto(syslog_msg, self.address)
            else:
                self.socket.sendall(syslog_msg)
        except Exception:
            self.handleError(record)
