FROM java:8-jdk-alpine

RUN apk add --no-cache wget

RUN adduser -D -g "" -h /home/szz/ -u 1000 szz

WORKDIR /home/szz/

USER szz

COPY py/szz/SZZUnleashed/SZZUnleashed.jar /home/szz/szz.jar

CMD ["sh"]

# BUILD docker build -f py/szz/SZZUnleashed/Dockerfile -t szz-unleashed:0.1.0 .
