import socket

host = 'localhost'
port = 1344
service = 'srv_clamav'

http_header = (
    "HTTP/1.0 200 OK\r\n"
    "Date: Fri, 06 Dec 2024 23:35:38 GMT\r\n"
    "\r\n"
)

request = (
    f"RESPMOD icap://{host}:{port}/{service} ICAP/1.0\r\n"
    f"Host: {host}\r\n"
    f"Allow: 204\r\n"
    f"Encapsulated: res-hdr=0, null-body={
        len(http_header.encode('utf-8'))}\r\n"
    f"\r\n"
    f"{http_header}"
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
