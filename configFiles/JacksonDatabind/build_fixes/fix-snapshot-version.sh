#/bin/bash
sed -i 's/2.4-SNAPSHOT</2.4.0</' pom.xml # For jackson-annotations
sed -i 's/-SNAPSHOT</</' pom.xml
sed -i 's/<!-- version from parent pom -->/<version>2.7.0-rc1<\/version>/' pom.xml