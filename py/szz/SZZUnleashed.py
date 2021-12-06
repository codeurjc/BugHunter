import json
import sys
import warnings

from injectable import load_injection_container
from py.framework.utils.utils import createDirIfNotExist
from py.szz.SZZ import SZZ

warnings.filterwarnings("ignore")

WORKDIR="/home/regseek/workdir"
MAX_CORES=1

class SZZUnleashed(SZZ):

    def __init__(self, project_name, bugId):
        SZZ.__init__(self, project_name, bugId, "SZZUnleashed")
        self._generateIssueInfo()

    def _generateIssueInfo(self):
        # Generate and save Issue info
        issue = {}
        issue[self.experiment_id] = {
            "creationdate": self.bug.bugConfig['issue_created_at'],
            "resolutiondate": self.bug.bugConfig['issue_closed_at'],
            "hash": self.bug.fixCommit,
            "commitdate":self.bug.bugConfig['fix_date']
        }

        with open(self.results_dir+"issue.json",'w+') as json_file:
            json.dump(issue, json_file, indent=4)

    def execute(self): 

        # Launch container with SZZ
        
        self.dockerClient.initContainer("szz-unleashed:0.1.0", self.experiment_id, workdir=self.results_dir)

        issue_path = self.results_dir+"/issue.json"
        project_path = WORKDIR+"/projects/"+self.experiment_id

        # Execute SZZ
        _, log = self.dockerClient.execute(
            self.experiment_id, 
            "java -jar /home/szz/szz.jar -i {issue_path} -r {project_path} -c {cores}".format(issue_path=issue_path, project_path=project_path, cores=MAX_CORES), 
            withTimeout=False
        )

        with open(self.log_path, "wb+") as out:
            out.write(log)

        self.dockerClient.shutdownContainers()

if __name__ == "__main__":

    load_injection_container(search_path="/home/regseek/workdir/py")

    if len(sys.argv) < 3:
        print("Use: python py/szz/SZZUnleashed.py <project_name> <bugId>")
        exit()

    szz = SZZUnleashed(sys.argv[1], str(sys.argv[2]))
    szz.execute()
