import re

def getTestName(cmd):
    
    if cmd.startswith("mvn"):
        return re.search(r"-Dtest=(.*) test",cmd).group(1)
    if cmd.startswith("ant"):
        return re.search(r"-Dtest.entry.method=(.*) run",cmd).group(1)
