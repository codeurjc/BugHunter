PROJECT=$1
BUG=$2
docker run -it -v $PWD:/home/jovyan/work/ \
    regression-seeker-analysis:0.1.1 \
    python analysis/Analysis.py $PROJECT $BUG