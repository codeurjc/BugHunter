if [ "$#" -ne 2 ]; then
    echo "Use: ./scripts/runExperiment.sh <project> <bug_id>"
    exit 1
fi
docker run -d \
    -v $PWD/configFiles:/home/regseek/workdir/configFiles \
    -v $PWD/results:/home/regseek/workdir/results \
    -v $PWD/py:/home/regseek/workdir/py \
    -v $PWD/projects:/home/regseek/workdir/projects \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -w /home/regseek/workdir/ \
    --name RS-$1-Bug-$2 \
    --privileged=true \
    regression-seeker:0.2.3 python py/RegTestExecutor.py $1 $2