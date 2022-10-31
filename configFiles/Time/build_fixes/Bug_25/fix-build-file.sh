#/bin/bash
if [ -d JodaTime/ ]; then
   cd JodaTime/ 
   mv * ../
   cd ../
fi
cp /home/regseek/workdir/configFiles/Time/build_fixes/Bug_25/build-552be4b677ec30a34d04d234395ba1a8c7beaacf.xml build.xml
cp /home/regseek/workdir/configFiles/Time/build_fixes/maven-build.xml maven-build.xml