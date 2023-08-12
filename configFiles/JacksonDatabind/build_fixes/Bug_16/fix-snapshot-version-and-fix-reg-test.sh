#/bin/bash
sed -i 's/2.4-SNAPSHOT</2.4.0</' pom.xml # For jackson-annotations
sed -i 's/-SNAPSHOT</</' pom.xml

if grep "ObjectMapper addMixIn" src/main/java/com/fasterxml/jackson/databind/ObjectMapper.java
then
    # code if found
    echo "addMixIn() EXISTS"
else
    # code if not found
    echo "addMixIn() NOT EXIST"
    git apply /home/regseek/workdir/configFiles/JacksonDatabind/build_fixes/Bug_16/addMixIn.patch
fi

