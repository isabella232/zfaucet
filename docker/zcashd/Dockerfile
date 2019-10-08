FROM debian:9

RUN apt-get update \
  && apt-get install -y gnupg2 apt-transport-https curl

ARG ZCASH_SIGNING_KEY_ID=6DEF3BAF272766C0
ARG ZCASH_VERSION=2.0.7+2
ARG ZCASHD_USER=zcashd

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys $ZCASH_SIGNING_KEY_ID \
  && echo "deb [arch=amd64] https://apt.z.cash/ jessie main" > /etc/apt/sources.list.d/zcash.list \
  && apt-get update \
  && apt-get install -y zcash=$ZCASH_VERSION

RUN adduser --quiet $ZCASHD_USER
ADD zcash.conf /home/$ZCASHD_USER/.zcash/zcash.conf
RUN chown -R $ZCASHD_USER:$ZCASHD_USER /home/$ZCASHD_USER
USER zcashd
WORKDIR /home/zcashd

HEALTHCHECK --interval=5m --timeout=3s \
    CMD zcash-cli getinfo || exit 1
