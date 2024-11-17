import socket
from icap_client import icap_reqmod

if __name__ == "__main__":
    icap_host = 'localhost'
    icap_port = 1344
    icap_service = 'srv_clamav'  # Replace with the correct service name
    http_request = (
        "GET / HTTP/1.1\r\n"
        "Host: localhost\r\n"
        "\r\n"
    )
    icap_reqmod(icap_host, icap_port, icap_service, http_request)
