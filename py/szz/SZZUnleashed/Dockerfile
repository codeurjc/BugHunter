FROM java:8-jdk-alpine

RUN apk add --no-cache wget

RUN adduser -D -g "" -h /home/szz/ -u 1000 szz

WORKDIR /home/szz/

USER szz

RUN wget -O szz.jar https://github.com/wogscpar/SZZUnleashed/blob/79f369fe2ccd2ae8c12d4e38edf71e7d988a8c68/examples/data/jars/szz_find_bug_introducers-0.1.jar?raw=true

CMD ["sh"]

# BUILD docker build -f py/szz/SZZUnleashed/Dockerfile -t szz-unleashed:0.1.0 .
