# Pull base image.
FROM python:3.9

ARG DOCKER_GID=999

# Install Docker

RUN curl -fsSL https://get.docker.com | sh

RUN pip install --upgrade pip
ADD py/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN useradd -m -u 1000 regseek

RUN addgroup --gid ${DOCKER_GID} dind && usermod -aG dind regseek

USER regseek
RUN mkdir /home/regseek/workdir/
VOLUME ["/home/regseek/workdir/"]
WORKDIR /home/regseek/workdir/

ENV PYTHONPATH="${PYTHONPATH}:/home/regseek/workdir/py/"

RUN echo "PS1='\[\033[1;36m\]RegressionSeeker-0.2.2 \[\033[1;34m\]\w\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" >> ~/.bashrc

CMD ["bash"]

# BUILD docker build --build-arg DOCKER_GID=999 -f dockerfiles/regression-seeker.Dockerfile -t regression-seeker:0.2.2 .