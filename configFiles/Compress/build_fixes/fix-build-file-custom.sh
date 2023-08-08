#/bin/bash
BUG_ID=$1
BUG_DIR="/home/regseek/workdir/configFiles/Compress/build_fixes/Bug_$BUG_ID/"
if [ -d $BUG_DIR ] 
then
    echo "Directory $BUG_DIR exists." 
else
    BFC_HASH=$(git rev-parse HEAD)
    mkdir $BUG_DIR
    cat /defects4j/framework/projects/Compress/build_files/$BFC_HASH/build.xml > $BUG_DIR/build.xml
    cat /defects4j/framework/projects/Compress/build_files/$BFC_HASH/maven-build.xml > $BUG_DIR/maven-build.xml
fi

cp $BUG_DIR/build.xml build.xml
cp $BUG_DIR/maven-build.xml maven-build.xml