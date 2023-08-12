FROM maven:3-jdk-8-slim

RUN \
  apt-get update -y && \
  apt-get install git -y && \
  rm -rf /var/lib/apt/lists/*

# BUILD docker build -f dockerfiles/maven.Dockerfile -t maven:3-jdk-8-slim-git dockerfiles/