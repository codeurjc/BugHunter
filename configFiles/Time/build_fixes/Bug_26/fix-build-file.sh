#/bin/bash
if [ -d JodaTime/ ]; then
   cd JodaTime/ 
   mv * ../
   cd ../
fi
cp /home/regseek/workdir/configFiles/Time/build_fixes/Bug_26/build-c7a581e55fc988bd90fa4bb1b0acece5181b7c5f.xml build.xml
cp /home/regseek/workdir/configFiles/Time/build_fixes/maven-build.xml maven-build.xml