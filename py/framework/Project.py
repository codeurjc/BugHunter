import json
import os
import shutil
from injectable import Autowired, autowired

from framework.utils.ProcessUtils import ProcessManager
from framework.utils.DockerUtils import DockerClient
from framework.utils.Defects4J import Defects4J
from framework.utils.GitUtils  import cloneRepository


class Project():
    
    @autowired
    def __init__(self, projectName, experimentId, bug, 
                    dockerClient: Autowired(DockerClient), processManager:Autowired(ProcessManager), d4j:Autowired(Defects4J)):
        
        with open('configFiles/{project}/project-config.json'.format(project=projectName)) as f:
            self.projectConfig = json.load(f)

        self.name = projectName
        self.bug = bug
        self.experimentId = experimentId
        self.repository = self.projectConfig['git_url']
        self.path = "{cwd}/projects/{experimentId}/".format(cwd=os.getcwd(), experimentId=self.experimentId)
        self.pm = processManager
        self.dockerImage = self.projectConfig['docker_image']
        self.dockerClient = dockerClient
        self.d4j = d4j

    def clone(self):
        if not os.path.isdir(self.path):
            if self.repository == "D4J":
                self.d4j.cloneRepository(self.name, self.experimentId, self.bug.id)
            else:
                cloneRepository(self.repository,self.path)

    def buildSource(self, resultsPath): 
        return self.executeOnCommit(self.bug.build_source_command , resultsPath + "source-build.log")

    def buildTests(self, resultsPath):
        return self.executeOnCommit(self.bug.build_test_command, resultsPath + "test-build.log")

    def executeTest(self, resultsPath):
        isSuccess = self.executeOnCommit(self.bug.test_command, resultsPath + "test-execution.log")
        if os.path.isfile(self.path+self.bug.test_report):
            shutil.copyfile(self.path+self.bug.test_report, resultsPath + "test-report.xml")
        else:
            self.pm.log("Test report not found!")
        return isSuccess

    def executeOnCommit(self, cmd, log_path):
    
        exit_code, log = self.dockerClient.execute(self.experimentId, cmd+" -Duser.home=$M2_FOLDER")

        with open(log_path, "wb+") as out:
            out.write(log)

        isSuccess = exit_code == 0
        
        if isSuccess:
            self.pm.log("   %s SUCCESS"%cmd)
        else:
            self.pm.log("   %s FAILS"%cmd)
        
        return isSuccess