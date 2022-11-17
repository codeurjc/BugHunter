#/bin/bash
if [ -f "src/test/java/org/apache/commons/codec/digest/DigestUtilsTest.java" ]; then
    echo "Deleting non-compiling test file"
    rm src/test/java/org/apache/commons/codec/digest/DigestUtilsTest.java
fi

if ! [ -f "build.xml" ]; then
    echo "No build.xml file found"
    cp /home/regseek/workdir/configFiles/Codec/build_fixes/default.build.xml build.xml
    cp /home/regseek/workdir/configFiles/Codec/build_fixes/maven-build.xml maven-build.xml
fi

if grep "compile.encoding" build.xml; then
    sed -i 's/${compile.encoding}/iso-8859-1/' build.xml
else
    sed -i 's/<javac/<javac encoding=\"iso-8859-1\"/' build.xml
fi
