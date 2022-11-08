#/bin/bash

# Fix double quotesin Java code
sed -i 's/<javac/<javac encoding=\"iso-8859-1\"/' build.xml