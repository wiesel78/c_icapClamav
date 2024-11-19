import socket


def icap_send_request(host, port, request, timeout = 10):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect((host, port))
        s.sendall(request)

        # Receive the response from the server
        response = b""
        while True:
            try:
                data = s.recv(1024)
                if not data:
                    break
                response += data
                if b"\r\n\r\n" in response:
                    break
            except socket.timeout:
                print("Socket timeout")
                break;

    return response.decode('utf-8')

def icap_options(host, port, service):
    # Build the ICAP OPTIONS request
    icap_request = (
        f"OPTIONS icap://{host}:{port}/{service} ICAP/1.0\r\n"
        f"Host: {host}\r\n"
        f"Encapsulated: null-body=0\r\n"
        f"\r\n"
    )

    response = icap_send_request(host, port, icap_request.encode('utf-8'))
    print(response)

def icap_reqmod(host, port, service, http_request):
    # Build the ICAP REQMOD request
    icap_request = (
        f"REQMOD icap://{host}:{port}/{service} ICAP/1.0\r\n"
        f"Host: {host}:{port}\r\n"
        f"Allow: 204\r\n"
        f"Encapsulated: req-hdr=0, null-body={len(http_request.encode('utf-8'))}\r\n"
        f"\r\n"
        f"{http_request}"
    )

    response = icap_send_request(host, port, icap_request.encode('utf-8'))
    print(response)

def icap_respmod(host, port, service, filename):
    # Read the file content
    try:
        with open(filename, 'rb') as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
        return

    # Construct the HTTP response headers
    http_response_headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/octet-stream\r\n"
        f"Content-Length: {len(file_content)}\r\n"
        "\r\n"
    ).encode('utf-8')

    # Combine headers and body to form the HTTP response
    http_response = http_response_headers + file_content

    # Calculate offsets for the Encapsulated header
    res_hdr_offset = 0
    res_body_offset = len(http_response_headers)

    # Construct the ICAP request headers
    icap_request_headers = (
        f"RESPMOD icap://{host}/{service} ICAP/1.0\r\n"
        f"Host: {host}\r\n"
        "Allow: 204\r\n"
        f"Encapsulated: res-hdr={res_hdr_offset}, res-body={res_body_offset}\r\n"
        f"Content-Length: {len(http_response)}\r\n"
        "\r\n"
    )

    # Combine ICAP headers and the encapsulated HTTP response
    icap_request = icap_request_headers.encode('utf-8') + http_response

    response = icap_send_request(host, port, icap_request)
    print(response)