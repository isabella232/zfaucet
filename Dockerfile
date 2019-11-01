FROM python:3
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

RUN chown -R zfaucet:zfaucet /app
USER zfaucet
ENTRYPOINT ["docker/zfaucet/entrypoint.sh"]

