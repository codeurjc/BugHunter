import json
import sys
import warnings
import datetime

from injectable import load_injection_container
from py.framework.utils.utils import createDirIfNotExist
from py.szz.SZZ import SZZ

warnings.filterwarnings("ignore")

WORKDIR="/home/regseek/workdir"

class PySZZ(SZZ):

    def __init__(self, project_name, bugId, algorithm):
        SZZ.__init__(self, project_name, bugId, "PySZZ_"+algorithm)
        self.algorithm = algorithm
        self._generateIssueInfo()
        self.gitManager.change_commit("master")

    def _generateIssueInfo(self):
        # Generate and save Issue info
        issues = []
        issues.append({
            "repo_name": "projects/"+self.experiment_id,
            "fix_commit_hash": self.bug.fixCommit,
            "best_scenario_issue_date": self._adaptDate(self.bug.bugConfig['issue_created_at'])
        })

        with open(self.results_dir+"issue.json",'w+') as json_file:
            json.dump(issues, json_file, indent=4)
    
    def _adaptDate(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S %z').strftime('%Y-%m-%dT%H:%M:%S')

    def execute(self): 

        # Launch container with SZZ
        
        self.dockerClient.initContainer("pyszz:0.1.1", self.experiment_id, workdir="/home/szz/")

        issue_path = self.results_dir+"issue.json"
        project_path = WORKDIR
        algorithm_config_path = WORKDIR+"/py/szz/PySZZ/conf/{algorithm}szz.yml".format(algorithm=self.algorithm)

        # Execute SZZ
        _, log = self.dockerClient.execute(
            self.experiment_id, 
            "python -u main.py {issue_path} {algorithm_config_path} {project_path}".format(
                issue_path=issue_path, 
                algorithm_config_path=algorithm_config_path, 
                project_path=project_path
            ), 
            withTimeout=False
        )
        # find . -name 'out/*json' -exec bash -c 'mv $0
        self.dockerClient.execute(self.experiment_id, "find out/ -type f -name '*json' -exec bash -c 'mv $0 "+self.results_dir+"result.json' {} \;", withTimeout=False)

        with open(self.log_path, "wb+") as out:
            out.write(log)

        self.dockerClient.shutdownContainers()

if __name__ == "__main__":

    load_injection_container(search_path="/home/regseek/workdir/py")

    if len(sys.argv) < 4:
        print("Use: python py/szz/PySZZ.py <project_name> <bugId> <algorithm>")
        exit()

    szz = PySZZ(sys.argv[1], str(sys.argv[2]), sys.argv[3])
    szz.execute()
