# Regression Seeker

## SetUp

#### Build images

Defects4J image
```
git clone https://github.com/rjust/defects4j.git tmp/defects4j/
cd tmp/defects4j/
git checkout v2.0.0
docker build -t defects4j:2.0.0 .
cd ../../
rm -rf tmp/defects4j/
```

RegressionSeeker image
```
docker build -f dockerfiles/regression-seeker.Dockerfile -t regression-seeker:0.2.1 .
```

> If in later steps the container generated from this image does not have permissions on Docker, you must build the image using the GID of the Docker socket as argument
```
DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
docker build --build-arg DOCKER_GID=$DOCKER_GID -f dockerfiles/regression-seeker.Dockerfile -t regression-seeker:0.2.1 .
```