cd py/szz/PySZZ/
if [ ! -d pyszz-master ]; then unzip pyszz.zip; fi
docker build -f Dockerfile -t pyszz:0.1.0 pyszz-master/
# /home/regseek/workdir/results/szz/PySZZ/JacksonCore_Bug_21_PySZZ/issue.json /home/regseek/workdir/py/szz/PySZZ/conf/agszz.yml /home/regseek/workdir/projects/