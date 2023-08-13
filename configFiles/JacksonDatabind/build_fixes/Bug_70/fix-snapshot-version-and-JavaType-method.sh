#/bin/bash
sed -i 's/2.4-SNAPSHOT</2.4.0</' pom.xml # For jackson-annotations
sed -i 's/-SNAPSHOT</</' pom.xml

if grep "getReferencedType" src/main/java/com/fasterxml/jackson/databind/JavaType.java
then
    # code if found
    echo "getReferencedType() EXISTS"
else
    # code if not found
    echo "getReferencedType() NOT EXIST"
    git apply /home/regseek/workdir/configFiles/JacksonDatabind/build_fixes/Bug_70/getReferencedType.patch
fi

