#!/bin/bash
# Read a string with spaces using for loop
ALGS=("ag" "l" "r" "ma" "ra")

while read reg; do
    for alg in ${ALGS[*]}
    do
        compact_reg=$(echo ${reg} | sed -r 's/\s+/_Bug_/g')

        if [ -d "results/szz/PySZZ_${alg}/${compact_reg}_PySZZ_${alg}" ] 
        then
            echo "ALREADY EXECUTED: results/szz/PySZZ_${alg}/${compact_reg}_PySZZ_${alg}" 
            continue
        else
            echo "Running ${compact_reg}_${alg}"
            compact_reg=$(echo ${reg} | sed -r 's/\s+/_/g')
            docker run -d \
                -v $PWD/configFiles:/home/regseek/workdir/configFiles \
                -v $PWD/results:/home/regseek/workdir/results \
                -v $PWD/py:/home/regseek/workdir/py \
                -v $PWD/projects:/home/regseek/workdir/projects \
                -v /var/run/docker.sock:/var/run/docker.sock \
                -w /home/regseek/workdir/ \
                --name $compact_reg-$alg \
                --privileged=true \
                regression-seeker:0.2.4 python py/szz/PySZZ.py $reg $alg
        fi
    done
done <scripts/regressions.txt