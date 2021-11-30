mkdir -p $PWD/szz_algorithms/SZZUnleashed/results/
docker run \
    -v $PWD/szz_algorithms/SZZUnleashed/issue_list_example.json:/home/szz/issue_list.json \
    -v $PWD/projects/Time_Bug_1:/home/szz/repository/ \
    -v $PWD/szz_algorithms/SZZUnleashed/results/:/home/szz/results/ \
    szz-unleashed:0.1.0 -i issue_list.json -r /home/szz/repository/