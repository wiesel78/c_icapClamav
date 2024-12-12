import socket

host = 'localhost'
port = 1344
service = 'srv_clamav'

content = (
    "i am bad\n"
)

content_len = len(content.encode('utf-8'))
hex_len = hex(content_len).replace("0x", "")

http_body = (
    f"{hex_len}\r\n"
    f"{content}\r\n"
    "0; ieof\r\n"
    "\r\n"
)

http_header = (
    "HTTP/1.0 200 OK\r\n"
    f"Content-Length: {content_len}\r\n"
    "\r\n"
)

http_header_length = len(http_header.encode('utf-8'))
request = (
    f"RESPMOD icap://{host}:{port}/{service} ICAP/1.0\r\n"
    f"Host: {host}\r\n"
    f"Allow: 204\r\n"
    f"Preview: {content_len}\r\n"
    f"Encapsulated: res-hdr=0, res-body={http_header_length}\r\n"
    f"\r\n"
    f"{http_header}"
    f"{http_body}"
)

print("Request:")
print(request)

print("Response:")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(request.encode('utf-8'))
    response = b""
    while True:
        data = s.recv(1024)
        if not data:
            break
        response += data

        if b"\r\n\r\n" in response:
            break

print(response.decode('utf-8', errors='ignore'))
