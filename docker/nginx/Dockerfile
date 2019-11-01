FROM nginx:1

RUN apt-get update && apt-get install -y openssl \
    && mkdir /ssl \
    && bash -c 'openssl req -x509 -nodes -newkey rsa:4096 \
      -keyout /ssl/faucet.testnet.z.cash-private.key \
      -out /ssl/faucet.testnet.z.cash.pem \
      -days 365 \
      -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=faucert.testnet.local" \
      -reqexts SAN \
      -config <(cat /etc/ssl/openssl.cnf \
            <(printf "\n[SAN]\nsubjectAltName=DNS:faucert.testnet.local,DNS:127.0.0.1"))'
  
ADD default.conf /etc/nginx/conf.d/default.conf
