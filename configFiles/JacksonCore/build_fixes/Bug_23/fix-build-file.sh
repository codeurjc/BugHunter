#/bin/bash
bash /home/regseek/workdir/configFiles/JacksonCore/build_fixes/fix-build-file.sh
rm -rf src/test/java/com/fasterxml/jackson/core/json/
rm -rf src/test/java/com/fasterxml/jackson/core/util/RequestPayloadTest.java