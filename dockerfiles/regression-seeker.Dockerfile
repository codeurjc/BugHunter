# Pull base image.
FROM python:3.9

# Install Docker

RUN curl -fsSL https://get.docker.com | sh

RUN pip install --upgrade pip
ADD py/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN useradd -m -u 1000 regseek && usermod -aG docker regseek
VOLUME ["/home/regseek/workdir/"]
WORKDIR /home/regseek/workdir/
USER regseek

RUN echo "PS1='\[\033[1;36m\]RegressionSeeker-0.1.0 \[\033[1;34m\]\w\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" >> ~/.bashrc

CMD ["bash"]

# BUILD docker build -f dockerfiles/regression-seeker.Dockerfile -t  regression-seeker:0.1.0 .
# RUN docker run -it --rm -v $PWD:/home/regseek/workdir/ -v /var/run/docker.sock:/var/run/docker.sock -w /home/regseek/workdir/ --name regression-seeker --privileged=true regression-seeker:0.1.0 bash