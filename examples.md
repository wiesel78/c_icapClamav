# ICAP examples

## Options

Request:

```http
OPTIONS icap://localhost:1344/srv_clamav ICAP/1.0
Host: localhost
Encapsulated: null-body=0
```

Response:

```http
ICAP/1.0 200 OK
Methods: RESPMOD, REQMOD
Service: C-ICAP/0.6.3 server - Antivirus service
ISTag: "CI0001-lus5dux6Dfo8zuARr+hPEwAA"
Transfer-Preview: *
Options-TTL: 3600
Date: Tue, 10 Dec 2024 21:26:25 GMT
Preview: 1024
Allow: 204
Encapsulated: null-body=0
```

## REQMOD

### REQMOD with HTTP header only

Request:

```http
REQMOD icap://localhost:1344/srv_clamav ICAP/1.0
Host: localhost:1344
Allow: 204
Encapsulated: req-hdr=0, null-body=35

GET / HTTP/1.1
Host: localhost
```

Response:

```http
ICAP/1.0 204 No Content
Server: C-ICAP/0.6.3
Connection: keep-alive
ISTag: "CI0001-lus5dux6Dfo8zuARr+hPEwAA"
```

### REQMOD with HTTP header and infected body

Request:

```http
REQMOD icap://localhost:1344/srv_clamav ICAP/1.0
Host: localhost
Encapsulated: req-hdr=0, req-body=82

POST / HTTP/1.1
Host: localhost
Pragma: no-cache
Transfer-Encoding: chunked

9
i am bad

0; ieof

```

Response:

```http
ICAP/1.0 200 OK
Server: C-ICAP/0.6.3
Connection: keep-alive
ISTag: "CI0001-lus5dux6Dfo8zuARr+hPEwAA"
X-Infection-Found: Type=0; Resolution=2; Threat=Trojan.Win32.TestInfectedFile.A.UNOFFICIAL;
X-Violations-Found: 1
        -
        Trojan.Win32.TestInfectedFile.A.UNOFFICIAL
        0
        0
Encapsulated: res-hdr=0, res-body=108

HTTP/1.0 403 Forbidden
Server: C-ICAP
Connection: close
Content-Type: text/html
Content-Language: en

1c7
<html>
 <head>
   <title>VIRUS FOUND</title>
</head>

<body>
<h1>VIRUS FOUND</h1>


You tried to upload/download a file that contains the virus:
   <b> Trojan.Win32.TestInfectedFile.A.UNOFFICIAL </b>
<br>
The Http location is:
<b>  localhost/ </b>

<p>
  For more information contact your system administrator

<hr>
<p>
This message generated by C-ICAP service: <b> srv_clamav?(null) </b>
<br>Antivirus engine: <b> clamd-122/0 </b>

</p>

</body>
</html>

0

```

### REQMOD with HTTP header and clean body

Request:

```http
REQMOD icap://localhost:1344/srv_clamav ICAP/1.0
Host: localhost
Encapsulated: req-hdr=0, req-body=82

POST / HTTP/1.1
Host: localhost
Pragma: no-cache
Transfer-Encoding: chunked

e
i am harmless

0; ieof

```

Response:

```http
ICAP/1.0 200 OK
Server: C-ICAP/0.6.3
Connection: keep-alive
ISTag: "CI0001-lus5dux6Dfo8zuARr+hPEwAA"
Encapsulated: req-hdr=0, req-body=141

POST / HTTP/1.1
Host: localhost
Pragma: no-cache
Transfer-Encoding: chunked
Via: ICAP/1.0 localhost (C-ICAP/0.6.3 Antivirus service )

e
i am harmless

0

```

## RESPMOD

### RESPMOD with HTTP header only

Request:

```http
RESPMOD icap://localhost:1344/srv_clamav ICAP/1.0
Host: localhost
Allow: 204
Encapsulated: res-hdr=0, null-body=56

HTTP/1.0 200 OK
Date: Fri, 06 Dec 2024 23:35:38 GMT

```

Response:

```http
RESPMOD icap://localhost:1344/srv_clamav ICAP/1.0
Host: localhost
Allow: 204
Encapsulated: res-hdr=0, null-body=56

HTTP/1.0 200 OK
Date: Fri, 06 Dec 2024 23:35:38 GMT

```

### Respmod with HTTP header and infected body

Request:

```http
RESPMOD icap://localhost:1344/srv_clamav ICAP/1.0
Host: localhost
Allow: 204
Preview: 9
Encapsulated: res-hdr=0, res-body=38

HTTP/1.0 200 OK
Content-Length: 9

9
i am bad

0; ieof

```

Response:

```http
ICAP/1.0 200 OK
Server: C-ICAP/0.6.3
Connection: keep-alive
ISTag: "CI0001-lus5dux6Dfo8zuARr+hPEwAA"
X-Infection-Found: Type=0; Resolution=2; Threat=Trojan.Win32.TestInfectedFile.A.UNOFFICIAL;
X-Violations-Found: 1
        -
        Trojan.Win32.TestInfectedFile.A.UNOFFICIAL
        0
        0
Encapsulated: res-hdr=0, res-body=167

HTTP/1.0 403 Forbidden
Server: C-ICAP
Connection: close
Content-Type: text/html
Content-Language: en
Via: ICAP/1.0 localhost (C-ICAP/0.6.3 Antivirus service )

1be
<html>
 <head>
   <title>VIRUS FOUND</title>
</head>

<body>
<h1>VIRUS FOUND</h1>


You tried to upload/download a file that contains the virus:
   <b> Trojan.Win32.TestInfectedFile.A.UNOFFICIAL </b>
<br>
The Http location is:
<b>  - </b>

<p>
  For more information contact your system administrator

<hr>
<p>
This message generated by C-ICAP service: <b> srv_clamav?(null) </b>
<br>Antivirus engine: <b> clamd-122/0 </b>

</p>

</body>
</html>

0

```

### Respmod with HTTP header and clean body

Request:

```http
RESPMOD icap://localhost:1344/srv_clamav ICAP/1.0
Host: localhost
Allow: 204
Preview: 14
Encapsulated: res-hdr=0, res-body=39

HTTP/1.0 200 OK
Content-Length: 14

e
i am harmless

0; ieof

```

Response:

```http
ICAP/1.0 204 No Content
Server: C-ICAP/0.6.3
Connection: keep-alive
ISTag: "CI0001-lus5dux6Dfo8zuARr+hPEwAA"

```

