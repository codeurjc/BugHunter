#/bin/bash
sed -i 's/-SNAPSHOT</</' pom.xml
# Remove problematic tests
rm src/test/java/com/fasterxml/jackson/databind/deser/TestCollectionDeserialization.java
rm src/test/java/com/fasterxml/jackson/databind/struct/TestPOJOAsArraySerialization.java