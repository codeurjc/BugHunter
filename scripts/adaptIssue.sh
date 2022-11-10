if [ "$#" -ne 2 ]; then
    echo "Use: ./scripts/adaptIssue.sh <project> <bug_id>"
    exit 1
fi

project=$1
bug_id=$2

echo "${project} ${bug_id}"
docker run --rm \
    -v $PWD/configFiles:/home/regseek/workdir/configFiles \
    -v $PWD/results:/home/regseek/workdir/results \
    -v $PWD/py:/home/regseek/workdir/py \
    -v $PWD/projects:/home/regseek/workdir/projects \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -w /home/regseek/workdir/ \
    --privileged=true \
    regression-seeker:0.2.4 \
    python py/szz/IssueAdapter.py $project $bug_id