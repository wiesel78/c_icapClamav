#!/bin/sh

# Send OPTIONS request to ICAP server
echo -ne "OPTIONS icap://localhost:1344/echo ICAP/1.0\r\nHost: localhost\r\n\r\n" | nc localhost 1344

# Send REQMOD request to ICAP server
echo -ne "REQMOD icap://localhost:1344/clamav ICAP/1.0\r\nHost: localhost\r\nEncapsulated: req-hdr=0, req-body=42\r\n\r\nGET / HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc localhost 1344 -v
