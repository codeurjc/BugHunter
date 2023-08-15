#!/bin/bash

while read reg; do
    compact_reg=$(echo ${reg} | sed -r 's/\s+/_Bug_/g')

    if [ -d "results/szz/OpenSZZ/${compact_reg}_OpenSZZ" ] 
    then
        echo "ALREADY EXECUTED: results/szz/OpenSZZ/${compact_reg}_OpenSZZ" 
        continue
    else
        echo "Running $compact_reg"
        docker run -d \
        -v $PWD/configFiles:/home/regseek/workdir/configFiles \
        -v $PWD/results:/home/regseek/workdir/results \
        -v $PWD/py:/home/regseek/workdir/py \
        -v $PWD/projects:/home/regseek/workdir/projects \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -w /home/regseek/workdir/ \
        --name $compact_reg-OpenSZZ \
        --privileged=true \
        regression-seeker:0.2.4 python py/szz/OpenSZZ.py $reg
    fi
done <scripts/regressions.txt