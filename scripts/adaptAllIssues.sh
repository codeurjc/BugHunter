for project in configFiles/*; do
    project_name=$(basename $project)
    for bug in $project/bugs/*; do
        bug=$(basename $bug)
        bug_id=$(echo $bug | sed -E 's/Bug_([0-9]*)\.json/\1/')

        echo "${project_name} ${bug_id}"
        docker run --rm \
            -v $PWD/configFiles:/home/regseek/workdir/configFiles \
            -v $PWD/results:/home/regseek/workdir/results \
            -v $PWD/py:/home/regseek/workdir/py \
            -v $PWD/projects:/home/regseek/workdir/projects \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -w /home/regseek/workdir/ \
            --privileged=true \
            regression-seeker:0.2.3 \
            python py/szz/IssueAdapter.py $project_name $bug_id
    done
done

