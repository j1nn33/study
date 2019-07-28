FROM alpine
RUN apk add --no-cache curl wget busybox-extras netcat-openbsd python py-pip && \
    pip install awscli && pip install md5
RUN apk --purge -v del py-pip
CMD tail -f /dev/null