import logging

from conftest import address, message


def test_info(adapter_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.info(message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_log(adapter_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - - \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.log(logging.INFO, message)
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_msgid(adapter_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' SUPER_DUPER_ID - \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.info(message, msgid="SUPER_DUPER_ID")
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)


def test_sd(adapter_with_udp_handler):
    expected_msg = (b'<14>1 2000-01-01T17:11:11.111111+06:00 testhostname root 111'
                    b' - [my_sd_id@32473 my_key="my_value"] \xef\xbb\xbfThis is an interesting message')
    adapter, syslog_socket = adapter_with_udp_handler
    adapter.info(message,
                 structured_data={'my_sd_id@32473': {'my_key': 'my_value'}})
    syslog_socket.sendto.assert_called_once_with(expected_msg, address)
