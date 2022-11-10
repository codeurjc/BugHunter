#!/bin/bash

while read reg; do
    echo "$reg-SZZUnleashed"
    compact_reg=$(echo ${reg} | sed -r 's/\s+/_/g')
    docker run -d \
        -v $PWD/configFiles:/home/regseek/workdir/configFiles \
        -v $PWD/results:/home/regseek/workdir/results \
        -v $PWD/py:/home/regseek/workdir/py \
        -v $PWD/projects:/home/regseek/workdir/projects \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -w /home/regseek/workdir/ \
        --name $compact_reg-SZZUnleashed \
        --privileged=true \
        regression-seeker:0.2.4 python py/szz/SZZUnleashed.py $reg
done <scripts/regressions.txt