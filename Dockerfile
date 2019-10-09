FROM python:2
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt && \
    pip install -r requirements-prod.txt  

RUN useradd -d /home/zfaucet -s /bin/bash zfaucet \
    && mkdir -p /home/zfaucet \
    && mkdir -p /home/zcashd/zfaucet/faucet/static \
    && chown zfaucet /app/faucet/migrations \
    && chown zfaucet /home/zcashd/zfaucet/faucet/static

RUN mkdir -p /app/lib/pyZcash \
    && git clone https://github.com/zcash-hackworks/pyZcash.git /app/lib/pyZcash/ 

USER zfaucet
ENTRYPOINT ["docker/zfaucet/entrypoint.sh"]

