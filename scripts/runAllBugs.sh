
project=$1

for bug in configFiles/$project/bugs/*; do
    bug=$(basename $bug)
    bug_id=$(echo $bug | sed -E 's/Bug_([0-9]*)\.json/\1/')

    if [[ ! -d results/$project/Bug_$bug_id ]]
    then
        echo "Bug_${bug_id}"
        ./scripts/runExperiment.sh $project $bug_id
    fi
done
