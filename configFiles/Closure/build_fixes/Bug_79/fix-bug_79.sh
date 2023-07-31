sed -i 's/<javac/<javac encoding=\"iso-8859-1\"/' build.xml
cp /home/regseek/workdir/configFiles/Closure/build_fixes/Bug_79/CompilerTestCase.java test/com/google/javascript/jscomp/CompilerTestCase.java
