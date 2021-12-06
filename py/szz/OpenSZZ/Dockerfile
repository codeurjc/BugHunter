FROM java:8-jdk-alpine

RUN apk add --no-cache wget && apk --no-cache add git

RUN adduser -D -g "" -h /home/szz/ -u 1000 szz

WORKDIR /home/szz/

USER szz

COPY py/szz/OpenSZZ/OpenSZZ.jar /home/szz/szz.jar

CMD ["sh"]

# BUILD docker build -f py/szz/OpenSZZ/Dockerfile -t openszz:0.1.0 .
