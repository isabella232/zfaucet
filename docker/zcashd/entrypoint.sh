#!/bin/bash

set -ex
set -o pipefail

zcash-fetch-params
ln -sf /dev/stderr .zcash/debug.log
touch .zcash/zcash.conf