FROM ubuntu:20.04

MAINTAINER ngocpq <phungquangngoc@gmail.com>

#############################################################################
# Requirements
#############################################################################

RUN \
  apt-get update -y && \
  apt-get install software-properties-common -y && \
  apt-get update -y && \
  apt-get install -y openjdk-8-jdk \
                git \
                build-essential \
				subversion \
				perl \
				curl \
				unzip \
				cpanminus \
				make \
                && \
  rm -rf /var/lib/apt/lists/*

# Java version
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# Timezone
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


#############################################################################
# Setup Defects4J
#############################################################################

# ----------- Step 1. Clone defects4j from github --------------
WORKDIR /
RUN git clone https://github.com/rjust/defects4j.git defects4j

# ----------- Step 2. Initialize Defects4J ---------------------
WORKDIR /defects4j
RUN cpanm --installdeps .
RUN ./init.sh

# ----------- Step 3. Add Defects4J's executables to PATH: ------
ENV PATH="/defects4j/framework/bin:${PATH}"  
#--------------

# EXTRA STEP - Use custom build.xml

COPY dockerfiles/defects4j/defects4j.build.xml /defects4j/framework/projects/defects4j.build.xml

RUN useradd -m -u 1000 regseek

COPY dockerfiles/defects4j/ant /usr/local/bin/
RUN chmod a+x /usr/local/bin/ant

USER regseek

#RUN echo "alias ant='/defects4j/major/bin/ant -f /defects4j/framework/projects/defects4j.build.xml -Dd4j.home=/defects4j -Dd4j.dir.projects=/defects4j/framework/projects -Dbasedir=$(pwd) -Dbuild.compiler=javac1.7 '" >> ~/.bashrc

# BUILD: docker build -f dockerfiles/defects4j/defects4j.Dockerfile -t defects4j:2.1.0 .