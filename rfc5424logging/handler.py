# coding=utf-8
import datetime
import socket
from codecs import BOM_UTF8
from collections import OrderedDict
from logging.handlers import SysLogHandler, SYSLOG_UDP_PORT

from tzlocal import get_localzone

NILVALUE = '-'

SP = b' '
# As defined in RFC5424 Section 7
REGISTERED_SD_IDs = ('timeQuality', 'origin', 'meta')
SYSLOG_VERSION = '1'

EMERGENCY = 70
EMERG = EMERGENCY
ALERT = 60
NOTICE = 25


class Rfc5424SysLogHandler(SysLogHandler):
    """
    A handler class which sends RFC 5424 formatted logging records to a syslog server.
    """
    # RFC6587 framing
    FRAMING_OCTET_COUNTING = 1
    FRAMING_NON_TRANSPARENT = 2

    # From the SysLogHandler class but extended with NOTICE, ALERT end EMERGENCY
    priority_map = {
        "DEBUG": "debug",
        "INFO": "info",
        "NOTICE": "notice",
        "WARNING": "warning",
        "ERROR": "error",
        "CRITICAL": "critical",
        "ALERT": "alert",
        "EMERGENCY": "emerg",
        "EMERG": "emerg",
    }

    def __init__(self, address=('localhost', SYSLOG_UDP_PORT),
                 facility=SysLogHandler.LOG_USER,
                 socktype=socket.SOCK_DGRAM,
                 framing=FRAMING_NON_TRANSPARENT,
                 hostname=None, appname=None, procid=None, structured_data=None, enterprise_id=None):
        """
        Returns a new instance of the Rfc5424SysLogHandler class intended to communicate with
        a remote machine whose address is given by address in the form of a (host, port) tuple.
        If address is not specified, ('localhost', 514) is used. The address is used to open a
        socket. An alternative to providing a (host, port) tuple is providing an address as a
        string, for example '/dev/log'. In this case, a Unix domain socket is used to send the
        message to the syslog. If facility is not specified, LOG_USER is used. The type of
        socket opened depends on the socktype argument, which defaults to socket.SOCK_DGRAM
        and thus opens a UDP socket. To open a TCP socket (for use with the newer syslog
        daemons such as rsyslog), specify a value of socket.SOCK_STREAM.

        Note that if your server is not listening on UDP port 514, SysLogHandler may appear
        not to work. In that case, check what address you should be using for a domain socket
        - it's system dependent. For example, on Linux it's usually '/dev/log' but on OS/X
        it's '/var/run/syslog'. You'll need to check your platform and use the appropriate
        address (you may need to do this check at runtime if your application needs to run
        on several platforms). On Windows, you pretty much have to use the UDP option.

        Args:
            address (tuple):
                address in the form of a (host, port) tuple
            facility (int):
                One of the Rfc5424SysLogHandler.LOG_* values.
            socktype (int):
                One of socket.SOCK_STREAM (TCP) or socket.SOCK_DGRAM (UDP).
            framing (int):
                One of the Rfc5424SysLogHandler.FRAMING_* values according to
                RFC6587 section 3.4. Only applies when sockettype is socket.SOCK_STREAM (TCP)
                and is used to give the syslog server an indication about the boundaries
                of the message. Defaults to FRAMING_NON_TRANSPARENT which will escape all
                newline characters in the message and end the message with a newline character.
                When set to FRAMING_OCTET_COUNTING, it will prepend the message length to the
                begin of the message.
            hostname (str):
                The hostname of the system where the message originated from.
                Defaults to `socket.gethostname()`
            appname (str):
                The name of the application. Defaults to the name of the logger that sent
                the message.
            procid (any):
                The process ID of the sending application. Defaults to the `process` attribute
                of the log record.
            structured_data (dict):
                A dictionary with structured data that is added to every message. Per message your
                can add more structured data by adding it to the `extra` argument of the log function.
            enterprise_id (int):
                Then Private Enterprise Number. This is used to compose the structured data IDs when
                they do not include an Enterprise ID and are not one of the reserved structured data IDs
        """
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

        super(Rfc5424SysLogHandler, self).__init__(address, facility, socktype)

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
        return str(ent_id)

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

            # Clean key-value pairs
            for (param_name, param_value) in sd_params:
                param_name = param_name.replace('=', '').replace(' ', '').replace(']', '').replace('"', '')
                param_value = param_value.replace('\\', '\\\\').replace('"', '\\"').replace(']', '\\]')

                param_name = param_name.encode('ascii', 'replace')[:32]
                param_value = param_value.encode('utf-8')

                sd_param = b''.join((param_name, b'="', param_value, b'"'))
                cleaned_sd_params.append(sd_param)

            cleaned_sd_params = SP.join(cleaned_sd_params)

            # Clean structured data ID
            sd_id = sd_id.replace('=', '').replace(' ', '').replace(']', '').replace('"', '')
            if '@' not in sd_id and sd_id not in REGISTERED_SD_IDs:
                sd_id = '@'.join((sd_id, enterprise_id))
            sd_id = sd_id.encode('ascii', 'replace')[:32]

            # build structured data element
            spacer = SP if cleaned_sd_params else b''
            sd_element = b''.join((b'[', sd_id, spacer, cleaned_sd_params, b']'))
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
            if self.framing == Rfc5424SysLogHandler.FRAMING_NON_TRANSPARENT:
                msg = msg.replace(b'\n', b'\\n')
                syslog_msg = SP.join((header, structured_data, msg))
                syslog_msg = b''.join((syslog_msg, b'\n'))
            else:
                syslog_msg = SP.join((header, structured_data, msg))
                syslog_msg = SP.join((str(len(syslog_msg)).encode('ascii'), syslog_msg))
        else:
            syslog_msg = SP.join((header, structured_data, msg))

        # Off it goes
        # Copied from SysLogHandler
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
