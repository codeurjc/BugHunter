import sys
import datetime

from injectable import load_injection_container
from py.szz.SZZ import SZZ

WORKDIR="/home/regseek/workdir"

class OpenSZZ(SZZ):

    def __init__(self, project_name, bugId):
        SZZ.__init__(self, project_name, bugId, "OpenSZZ")

    def _dateToMillis(self, date_raw):
        epoch = datetime.datetime.utcfromtimestamp(0)
        date = datetime.datetime.strptime(date_raw, '%Y-%m-%d %H:%M:%S %z').replace(tzinfo=None)
        return int((date - epoch).total_seconds() * 1000.0)

    def execute(self): 

        # Launch container with SZZ
        
        self.dockerClient.initContainer("openszz:0.1.0", self.experiment_id, workdir=self.results_dir)

        issue_created = self._dateToMillis(self.bug.bugConfig['issue_created_at'])
        project_path = WORKDIR+"/projects/"+self.experiment_id

        print(issue_created, self.bug.fixCommit)

        _, log = self.dockerClient.execute(
            self.experiment_id, 
            "java -jar /home/szz/szz.jar -bfc {bfc} -d {project_path} -i {issue_created} -o {results_output}".format(
                bfc=self.bug.fixCommit, project_path=project_path, issue_created=issue_created, results_output=self.results_dir 
            ), 
            withTimeout=False
        )

        with open(self.log_path, "wb+") as out:
            out.write(log)

        self.dockerClient.shutdownContainers()

if __name__ == "__main__":

    load_injection_container(search_path="/home/regseek/workdir/py")

    if len(sys.argv) < 3:
        print("Use: python py/szz/OpenSZZ.py <project_name> <bugId>")
        exit()

    szz = OpenSZZ(sys.argv[1], str(sys.argv[2]))
    szz.execute()
