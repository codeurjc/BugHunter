import json
import sys
from framework.utils.Defects4J  import Defects4J
from injectable import load_injection_container
import warnings
warnings.filterwarnings("ignore")

if len(sys.argv) < 2:
    print("Use: python py/ExtractBugsD4J.py <d4j_project_name>")
    exit()

load_injection_container()

project_name = sys.argv[1]
d4j = Defects4J()
# d4j.cloneRepository(project_name,project_name+"-EXAMPLE", 1)

with open('configFiles/{project}/project-config.json'.format(project=sys.argv[1])) as f:
    projectConfig = json.load(f)

for bug in d4j.getAllBugs(projectConfig['project']):
    d4j.generateBugConfigFile(projectConfig, bug)