git clone https://github.com/rjust/defects4j.git tmp/defects4j/
cd tmp/defects4j/
git checkout v2.0.0
docker build -t defects4j:2.0.0 .
cd ../../
rm -rf tmp/defects4j/