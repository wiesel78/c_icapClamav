import socket

host = 'localhost'
port = 1344
service = 'srv_clamav'

request = (
    f"OPTIONS icap://{host}:{port}/{service} ICAP/1.0\r\n"
    f"Host: {host}\r\n"
    f"Encapsulated: null-body=0\r\n"
    f"\r\n"
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
