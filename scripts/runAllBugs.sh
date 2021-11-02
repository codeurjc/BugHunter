
project=$1

for bug in configFiles/$project/bugs/*; do
    bug=$(basename $bug)
    bug_id=$(echo $bug | sed -E 's/Bug-([0-9]*)\.json/\1/')

    # if [[ ($bug_id == "46" )]]
    # then
    #     exit
    # fi

    if [[ ! -d results/$project/Bug_$bug_id ]]
    then
        echo "Bug_${bug_id}"
        ./scripts/runExperiment.sh $project $bug_id
    fi
done
