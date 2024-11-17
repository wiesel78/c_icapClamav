import socket
from icap_client import icap_options

if __name__ == "__main__":
    icap_host = 'localhost'
    icap_port = 1344
    icap_service = 'srv_clamav'  # Replace with the correct service name
    icap_options(icap_host, icap_port, icap_service)
