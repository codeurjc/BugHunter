#PROJECTS=("JacksonXml" "Time" "Collections" "Compress" "Csv" "JacksonCore" "JacksonDatabind" "Gson" "Jsoup" "Lang" "Math" "Closure" "Mockito")
PROJECTS=($1)

for project in ${PROJECTS[*]}; do

    for bug in configFiles/$project/bugs/*; do
        bug=$(basename $bug)
        bug_id=$(echo $bug | sed -E 's/Bug_([0-9]*)\.json/\1/')

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
    done
done