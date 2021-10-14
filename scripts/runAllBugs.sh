
project=$1

for bug in configFiles/$1/bugs/*; do
    bug=$(basename $bug)
    bug_id=$(echo $bug | sed -E 's/Bug-([0-9]*)\.json/\1/')
    ./scripts/runExperiment.sh $1 $bug_id
done
