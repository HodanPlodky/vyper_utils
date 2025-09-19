#!/bin/bash

RED='\033[0;31m'
GREEN='\033[1;32m'
NC='\033[0m'

cd "${VYPER_DIR}"
source "${CHECK_PYENV}"
for commit in "$@"
do
    printf "checking out $commit ..." 1>&2
    git checkout $commit 2> /dev/null > /dev/null


    if [ $? -ne 0 ]; 
    then
        printf " ${RED}commit does not exist"${NC}"\n"; 1>&2
        continue
    fi

    # this is because if the commit contains the backslash
    # it can create problems for file system
    commit=${commit//\//-}

    printf "filename,opt-codesize,opt-none" > "/tmp/${commit}.tmp.csv"

    if [ $? -ne 0 ]; 
    then
        printf " ${RED}error creating file${NC}\n"; 1>&2
        continue
    fi

    for file in ${TEST_DIR}/*.vy; do
        echo "" >> "/tmp/${commit}.tmp.csv"
        printf "${file}," >> "/tmp/${commit}.tmp.csv"
        PYTHONPATH=. python vyper/cli/vyper_compile.py  --enable-decimals --experimental-codegen ${file} 2> /dev/null | wc -c | tr -d "\n" >> "/tmp/${commit}.tmp.csv"
        printf "," >> "/tmp/${commit}.tmp.csv"
        PYTHONPATH=. python vyper/cli/vyper_compile.py  --enable-decimals --experimental-codegen ${file} --optimize none 2> /dev/null | wc -c | tr -d "\n" >> "/tmp/${commit}.tmp.csv"
    done

    printf " ${GREEN}done${NC}\n" 1>&2
done
