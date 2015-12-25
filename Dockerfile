FROM debian:jessie
MAINTAINER Yury Bilenkis <yura@ostrovok.ru>

RUN set -xe \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update -qq  \
    && apt-get install -qq \
            unzip \
            curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY image/ /image/
WORKDIR /image

RUN set -xe \
    && ZIPIMG=$(ls *.zip) \
    && if [ -e $ZIPIMG ] ; then \
            IMG=$(unzip -Z -1 "$ZIPIMG"); \
            unzip "$ZIPIMG"; \
       fi \

    && OFFSET=$(fdisk -lus $IMG | awk '/img2/ {print $2}') \
    && OFFSET=$OFFSET*512 \
    && mount -o loop,offset=$OFFSET,rw $IMG /mnt
