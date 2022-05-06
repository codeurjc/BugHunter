if [ "$#" -ne 1 ]; then
    echo "Use: ./scripts/runExtractBugsD4J.sh <project>"
    exit 1
fi
docker run -d \
    -v $PWD/configFiles:/home/regseek/workdir/configFiles \
    -v $PWD/results:/home/regseek/workdir/results \
    -v $PWD/py:/home/regseek/workdir/py \
    -v $PWD/projects:/home/regseek/workdir/projects \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -w /home/regseek/workdir/ \
    --name EXTRACT-BUGS-$1 \
    --privileged=true \
    regression-seeker:0.2.3 python py/ExtractBugsD4J.py <d4j_project_name>