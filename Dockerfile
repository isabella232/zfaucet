FROM python:2
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt && \
    pip install -r requirements-prod.txt  

ENTRYPOINT ["docker/zfaucet/entrypoint.sh"]