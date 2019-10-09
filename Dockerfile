FROM python:2
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt && \
    pip install -r requirements-prod.txt  

RUN useradd -d /home/zfaucet -s /bin/bash zfaucet \
    && mkdir -p /home/zfaucet \
    && chown zfaucet /app/faucet/migrations \
    && chown zfaucet /home/zcashd/zfaucet/faucet/static

RUN mkdir -p /app/lib/pyZcash \
    && git clone --branch ben/enable-rpc-params-in-env https://github.com/benzcash/pyZcash.git /app/lib/pyZcash/ 

USER zfaucet
ENTRYPOINT ["docker/zfaucet/entrypoint.sh"]

