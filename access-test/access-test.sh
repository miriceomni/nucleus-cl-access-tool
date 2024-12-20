#!/bin/bash

set -e


export CLIENT_LIB_SDK_DIR=/home/ubuntu/omniverse/nucleus-cl-access-tool/connect-sdk/connect-samples-205.0.0

export USD_LIB_DIR=${CLIENT_LIB_SDK_DIR}/_build/linux-x86_64/release
export PYTHON=${CLIENT_LIB_SDK_DIR}/_build/target-deps/python/python

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${USD_LIB_DIR}
export PYTHONPATH=${USD_LIB_DIR}/python:${USD_LIB_DIR}/bindings-python

if [ ! -f ${PYTHON} ]; then
    echo "echo Python, USD, and Omniverse Client libraries are missing.  Run \"./repo.sh build --stage\" to retrieve them."
    popd
    exit
fi

${PYTHON} access-test.py "$@"

