#/bin/bash
if [ -d "src/test/java/" ];
then
    echo "src/test/java/ exists"
    cp /home/regseek/workdir/configFiles/Cli/build_fixes/old_snapshots/default.build.xml build.xml
    if cat pom.xml | grep "junit</artifact" -A 1 | grep "<version>3"; then
        echo "Using junit 3"
        cp /home/regseek/workdir/configFiles/Cli/build_fixes/old_snapshots/maven-build-junit3.xml maven-build.xml
    else
        echo "Using junit 4"
        cp /home/regseek/workdir/configFiles/Cli/build_fixes/old_snapshots/maven-build.xml maven-build.xml
    fi
    if ! [ -d "src/test/resources/" ];
    then 
        sed -i 's/src\/test\/resources/\./' maven-build.xml
    fi
    
else
    if ! [ -d "src/java/org/apache/commons/cli2" ]; then
        echo "src/java/org/apache/commons/cli2 does not exist"
        cp /home/regseek/workdir/configFiles/Cli/build_fixes/old_snapshots/default.build.xml build.xml
        cp /home/regseek/workdir/configFiles/Cli/build_fixes/old_snapshots/maven-build-29.xml maven-build.xml
    else
        echo "Using basic config"
        cp /home/regseek/workdir/configFiles/Cli/build_fixes/default.build.xml build.xml
    fi
fi