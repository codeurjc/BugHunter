docker run -it --rm \
    -v $PWD/configFiles:/home/regseek/workdir/configFiles \
    -v $PWD/results:/home/regseek/workdir/results \
    -v $PWD/py:/home/regseek/workdir/py \
    -v $PWD/projects:/home/regseek/workdir/projects \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -w /home/regseek/workdir/ \
    --name regression-seeker \
    --privileged=true \
    regression-seeker:0.2.2 bash