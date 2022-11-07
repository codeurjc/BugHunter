if [ "$#" -ne 2 ]; then
    echo "Use: ./scripts/reRunExperiment.sh <project> <bug_id>"
    exit 1
fi

rm -rf projects/$1_Bug_$2/ 
rm -rf results/$1/Bug_$2/
docker rm -f RS-$1-Bug-$2
./scripts/runExperiment.sh $1 $2