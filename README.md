Dockerfile for building an image of ICAP enabled Antivirus server that is based on c-icap, clamav and Alpine Linux. 

As this is for **testing, researching and demonstration purposes only**, the
clamav antivirus database does not contain any valid virus signatures, thus it
will not detect any viruses. Again for the same purpose one may want to
simulate a file being blocked by the antivirus engine. For that a custom
antivirus signature is added that will recognize a particular and well known
good file as a virus. That file is putty.exe. So if you want to
test/demonstrate a file blocked by ICAP just transfer your
putty.exe to the server.

**Freshclam** is also available to download actual antivirus definition
files in case they are needed.

## Disclaimer

This is a fork of [https://github.com/nkapashi/c_icapClamav](https://github.com/nkapashi/c_icapClamav)

## Build and run

### Clone the repository

```bash
git clone https://github.com/wiesel78/c_icapClamav.git
```

### Docker Compose

Build and start the container using docker-compose:

```bash
docker-compose up -d
```

### Docker

Build the image:

```bash
docker build -t icap .
```

Start the container:

```bash
docker run -p 1344:1344 --name icap -it icap
```

After all services are started the container will give a shell access. All scan
activity is under the /var/log/c-icap/access.log.

## Add custom signature

To add a custom signature to the clamav database, you need to add the hex
representation of the file or part of the file to the custom_vir_sig.ndb file.
Here we create a file and build the ndb row for the created file, so clamav can
identify it as a infected file. We will do this inside the container so we can
use the clamscan command to instantly check if the file is detected as a virus.

```bash
docker-compose exec icap-clamav bash
```

create the custom file. You can use any file you want, but for this example we
will create a simple text file with the content "i am infected".

```bash
echo "i am infected" > /tmp/infected-file.txt
```

Now we will create the ndb row for the file. The signature is the hex
representation of the file. We can use xxd to get the hex string of any file.

```bash
testsignature=$(xxd -p /tmp/infected-file.txt)
echo "Trojan.Win32.TestInfectedFile.A:0:*:${testsignature}" >> /var/lib/clamav/custom_vir_sig.ndb
```

The ndb row format, defined in
[clamav signatures](https://docs.clamav.net/manual/Signatures/ExtendedSignatures.html)
, is:

```bash
MalwareName:TargetType:Offset:HexSignature[:min_flevel:[max_flevel]]
```

Test the signature with clamscan:

```bash
clamscan /tmp/infected-file.txt
```
