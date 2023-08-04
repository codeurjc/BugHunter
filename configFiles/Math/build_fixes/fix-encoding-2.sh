#/bin/bash
if grep -wq "source.encoding" build.xml; then 
    echo "Encoding already exist" 
else 
    sed -i 's/<javac/<javac encoding=\"iso-8859-1\"/' build.xml
fi