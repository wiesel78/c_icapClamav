FROM alpine:latest

# Set the version of c-icap and c-icap-modules you wish to use
ENV cicapVersion="0.6.3" cicapModuleVersion="0.5.7"

WORKDIR /

RUN mkdir -p /tmp/install && \
    mkdir -p /opt/c-icap && \
    mkdir -p /var/log/c-icap && \
    mkdir -p /run/clamav && \
    cd /tmp/install 

RUN apk --update --no-cache add \
        bzip2 \
        bzip2-dev \
        zlib \
        zlib-dev \
        curl \
        tar \
        gcc \
        make \
        g++ \
        clamav \
        clamav-libunrar \
        libatomic \
        git \
        autoconf \
        automake \
        libtool && \
    git config --global --add advice.detachedHead false

# Download and build c-icap
RUN git clone --branch C_ICAP_0.6.3 --depth 1 https://github.com/c-icap/c-icap-server.git && \
    cd c-icap-server && \
    autoreconf -i && \
    ./configure --quiet --prefix=/opt/c-icap --enable-large-files && \
    make && \
    make install && \
    cd /tmp/install

# # Download and build c-icap-modules
RUN git clone --branch C_ICAP_MODULES_0.5.7 --depth 1 https://github.com/c-icap/c-icap-modules.git && \
    cd c-icap-modules && \
    autoreconf -i && \
    ./configure --quiet --with-c-icap=/opt/c-icap --prefix=/opt/c-icap && \
    make && \
    make install && \
    cd /tmp/install

# # configure clamav
RUN chown clamav:clamav /run/clamav && \
    sed -i 's/^#Foreground .*$/Foreground yes/g' /etc/clamav/clamd.conf && \
    sed -i 's/^#Foreground .*$/Foreground yes/g' /etc/clamav/freshclam.conf && \
    sed -i 's/#MaxAttempts .*$/MaxAttempts 5/g' /etc/clamav/freshclam.conf && \
    sed -i 's/#DatabaseMirror .*$/DatabaseMirror db.US.clamav.net/g' /etc/clamav/freshclam.conf 

RUN cd && \
    rm -rf /tmp/install && \
    apk del \
        bzip2 \
        bzip2-dev \
        zlib \
        zlib-dev \
        curl \
        tar \
        gcc \
        make \
        g++ \
        git \
        autoconf \
        automake \
        libtool && \
    rm -rf /opt/c-icap/etc/*.default

COPY ./etc /opt/c-icap/etc
COPY ./opt/ /opt
COPY ./signatures/custom_vir_sig.ndb /var/lib/clamav/custom_vir_sig.ndb
RUN chmod +x /opt/start.sh

EXPOSE 1344

CMD ["/bin/sh", "-c", "/opt/start.sh && tail -f /dev/null"]

