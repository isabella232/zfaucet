#!/bin/bash

set -ex
set -o pipefail

env | sort
zcash-fetch-params


export ZCASHD_CMD='zcashd -printtoconsole -checkblocks=288'
if [[ ! -z "${ZCASHD_NETWORK}" ]];then ZCASHD_CMD+=" -testnet -addnode=testnet.z.cash ";fi
if [[ ! -z "${ZCASHD_SHOWMETRICS}" ]];then ZCASHD_CMD+=" -showmetrics=1";fi
if [[ ! -z "${ZCASHD_LOGIPS}" ]];then ZCASHD_CMD+=" -logips=1";fi
if [[ ! -z "${ZCASHD_EXPERIMENTALFEATURES}" ]];then ZCASHD_CMD+=" -experimentalfeatures=1";fi
if [[ ! -z "${ZCASHD_GEN}" ]];then ZCASHD_CMD+=" -gen=${ZCASHD_GEN}";fi
if [[ ! -z "${ZCASHD_ZSHIELDCOINBASE}" ]];then ZCASHD_CMD+=" -zshieldcoinbase=1";fi
if [[ ! -z "${ZCASHD_RPCUSER}" ]];then ZCASHD_CMD+=" -rpcuser=${ZCASHD_RPCUSER}";fi
if [[ ! -z "${ZCASHD_RPCPASSWORD}" ]];then ZCASHD_CMD+=" -rpcpassword=${ZCASHD_RPCPASSWORD}";fi
if [[ ! -z "${ZCASHD_RPCBIND}" ]];then ZCASHD_CMD+=" -rpcbind=${ZCASHD_RPCBIND}";fi
if [[ ! -z "${ZCASHD_ALLOWIP}" ]];then ZCASHD_CMD+=" -rpcallowip=${ZCASHD_ALLOWIP}";fi

if [[ "${ZCASHD_NETWORK}" == "testnet" ]];then
mkdir -p .zcash/testnet3
rm -f .zcash/testnet3/debug.log
fi
touch .zcash/zcash.conf

echo "Starting: ${ZCASHD_CMD}"
${ZCASHD_CMD}