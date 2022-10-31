#/bin/bash
bash /home/regseek/workdir/configFiles/Jsoup/build_fixes/fix-build-file.sh
# Copy aux file
cp /home/regseek/workdir/configFiles/Jsoup/build_fixes/Bug_78/InterruptedServlet.java src/test/java/org/jsoup/integration/servlets/InterruptedServlet.java
# Copy modified regression test
cp /home/regseek/workdir/configFiles/Jsoup/build_fixes/Bug_78/ConnectTest.java src/test/java/org/jsoup/integration/ConnectTest.java