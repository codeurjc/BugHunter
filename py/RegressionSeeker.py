from DockerUtils import DockerClient
from ProcessUtils import ProcessManager
from Defects4J import Defects4J
import os
import sys
import json
import uuid

class RegressionSeeker():

    def __init__(self, projectConfig, bug_id):
        self.projectConfig = projectConfig

        # CREATE RESULTS FOLDER IF NOT EXIST
        project_results_folder = "results/%s" % (projectConfig['project'])
        if not os.path.isdir(project_results_folder): 
            os.makedirs(project_results_folder)
            os.makedirs(project_results_folder+"/RegressionSeekerLogs/")

        # CREATE BUG FOLDER IF NOT EXIST
        bug_folder = "results/%s/Bug_%d/" % (projectConfig['project'], bug_id)
        if not os.path.isdir(bug_folder): os.makedirs(bug_folder)

        # CREATE PROCESS MANAGER
        self.pm = ProcessManager(open(project_results_folder+"/RegressionSeekerLogs/RegressionSeeker-Bug_"+str(bug_id)+".log", 'w+'), "REGRESSION SEEKER")
        self.pm.log("Starting process")

        # CREATE DOCKER MANAGER
        # self.pm = ProcessManager(open(bug_folder+"RegressionSeeker.log", 'w+'), "REGRESSION SEEKER")
        # self.pm.log("Starting process")

        # IF PROJECT DOES NOT EXIST -> CLONE
        if not os.path.isdir(projectConfig['project']):

            if projectConfig['git_url'] == "D4J":
                d4j = Defects4J(container_name="defects4j-container-"+projectConfig['project']+str(bug_id)+str(uuid.uuid4()))
                self.pm.log("Cloning repository from Defects4J")
                _, out = d4j.cloneRepository(projectConfig['project'],)
                self.pm.log(out)
            else:
                pass # TODO: Implement case of real Git URL

        # CREATE FOLDERS PER COMMIT
        

    def close(self):
        self.pm.close()


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Use: python py/RegressionSeeker.py <project_name>")
        exit()

    with open('configFiles/{project}/project-config.json'.format(project=sys.argv[1])) as f:
        projectConfig = json.load(f)

    rs = RegressionSeeker(projectConfig, 1)