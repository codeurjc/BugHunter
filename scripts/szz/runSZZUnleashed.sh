#!/bin/bash

while read reg; do
    compact_reg=$(echo ${reg} | sed -r 's/\s+/_Bug_/g')

    if [ -f "results/szz/SZZUnleashed/${compact_reg}_SZZUnleashed/SZZUnleashed.log" ] 
    then
        echo "ALREADY EXECUTED: results/szz/SZZUnleashed/${compact_reg}_SZZUnleashed" 
        continue
    else
        echo "Running $compact_reg"
        # rm -rf projects/${compact_reg}_SZZUnleashed/
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
    fi
done <scripts/regressions.txt