
project=$1
count=0

for bug in configFiles/$project/bugs/*; do
    bug=$(basename $bug)
    bug_id=$(echo $bug | sed -E 's/Bug_([0-9]*)\.json/\1/')


    if [[ ! -d results/$project/Bug_$bug_id ]]
    then
        echo "Bug_${bug_id}"
        ((count=count+1))
        ./scripts/runExperiment.sh $project $bug_id
    fi

    if (( $count > 64 )); then
        exit
    fi

done
