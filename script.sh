#!/usr/bin/env bash

set -ex

if [ -n "${DOMERGE}" ]; then
    docker run dockershelf/pypicontents:2.7 pypicontents --version
    docker run -v ${PWD}:${PWD} -w ${PWD} \
        dockershelf/pypicontents:2.7 \
            pypicontents merge -o pypi.json -i data
    docker run -v ${PWD}:${PWD} -w ${PWD} \
        dockershelf/pypicontents:2.7 \
            pypicontents merge -o stdlib.json -i stdlib
    docker run -v ${PWD}:${PWD} -w ${PWD} \
        dockershelf/pypicontents:2.7 \
            pypicontents errors -o errors.json -i logs
    docker run -v ${PWD}:${PWD} -w ${PWD} \
        dockershelf/pypicontents:2.7 \
            pypicontents stats -o stats.txt -i logs
fi

if [ -n "${LRANGE}" ]; then

    if [ "${LRANGE}" == "p" ]; then
        set +e
    fi

    docker run dockershelf/pypicontents:2.7-3.5 pypicontents --version
    docker run -v ${PWD}:${PWD} -v ${HOME}/.cache/pip:/root/.cache/pip \
        -w ${PWD} dockershelf/pypicontents:2.7-3.5 \
            pypicontents pypi -o data/${LRANGE}/pypi.json \
                -f logs/${LRANGE}/pypi.log -R ${LRANGE}
fi

if [ -n "${PYVER}" ]; then
    docker run dockershelf/pypicontents:${PYVER} pypicontents --version
    docker run -v ${PWD}:${PWD} -w ${PWD} \
        dockershelf/pypicontents:${PYVER} \
            pypicontents stdlib -o stdlib/${PYVER}/stdlib.json
fi

sudo chown -R ${USER}:${USER} stdlib data logs *.json *.txt