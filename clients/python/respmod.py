import socket
from icap_client import icap_respmod

if __name__ == "__main__":
    icap_host = 'localhost'
    icap_port = 1344
    icap_service = 'srv_clamav' 
    filename = 'test_file.txt'

    icap_respmod(icap_host, icap_port, icap_service, filename)
