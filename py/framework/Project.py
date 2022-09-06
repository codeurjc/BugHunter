import re
import os
import shutil
from injectable import Autowired, autowired
from junitparser import JUnitXml, Failure, Error, Skipped

from framework.utils.ProcessUtils import ProcessManager
from framework.utils.DockerUtils import DockerClient
from framework.utils.Defects4J import Defects4J
from framework.utils.GitUtils  import cloneRepository


class Project():
    
    @autowired
    def __init__(self, projectName, experimentId, bug, 
                    dockerClient: Autowired(DockerClient), processManager:Autowired(ProcessManager), d4j:Autowired(Defects4J)):

        self.name = projectName
        self.bug = bug
        self.experimentId = experimentId
        self.repository = self.bug.bugConfig['git_url']
        self.path = "{cwd}/projects/{experimentId}/".format(cwd=os.getcwd(), experimentId=self.experimentId)
        self.pm = processManager
        self.dockerImage = self.bug.bugConfig['docker_image']
        self.dockerClient = dockerClient
        self.d4j = d4j

    def clone(self):
        if not os.path.isdir(self.path):
            if self.repository == "D4J":
                self.d4j.cloneRepository(self.name, self.experimentId, self.bug.id)
            else:
                cloneRepository(self.repository,self.path)

    def applyFixes(self, resultsPath):
        if 'fixes' in self.bug.bugConfig:
            fix_cmd = self.bug.bugConfig['fixes']
            self.pm.log("Applying fixes: %s"%fix_cmd)
            self.executeOnCommit(fix_cmd, resultsPath + "apply-fixes.log")

    def buildSource(self, resultsPath): 
        return self.executeOnCommitWithJava(self.bug.build_source_command, resultsPath + "source-build.log")

    def buildTests(self, resultsPath):
        return self.executeOnCommitWithJava(self.bug.build_test_command, resultsPath + "test-build.log")

    def executeTest(self, resultsPath):
        isSuccess = self.executeOnCommitWithJava(self.bug.test_command, resultsPath + "test-execution.log")
        if os.path.isfile(self.path+self.bug.test_report):
            shutil.copyfile(self.path+self.bug.test_report, resultsPath + "test-report.xml")
        else:
            self.pm.log("Test report not found!")
        return isSuccess

    def executeOnCommitWithJava(self, cmd, log_path):
        return self.executeOnCommit(cmd+" -Duser.home=$M2_FOLDER", log_path)

    def executeOnCommit(self, cmd, log_path):
    
        exit_code, log = self.dockerClient.execute(self.experimentId, cmd)

        with open(log_path, "wb+") as out:
            out.write(log)

        isSuccess = exit_code == 0
        
        if isSuccess:
            self.pm.log("   %s SUCCESS"%cmd)
        else:
            self.pm.log("   %s FAILS"%cmd)
        
        return isSuccess
    
    def getTestReportResult(self, resultsPath):
        
        test_name = ""

        if self.bug.test_command.startswith("mvn"):
            test_name = re.search(r"-Dtest=(.*) test",self.bug.test_command).group(1)
        if self.bug.test_command.startswith("ant"):
            test_name = re.search(r"-Dtest.entry.method=(.*) run",self.bug.test_command).group(1)

        method_name = test_name.split("#")[1]

        xml = JUnitXml.fromfile(resultsPath+"test-report.xml")
        for case in xml:
            #print(case.name +"=="+method_name)
            if case.name == method_name:
                for elem in case:
                    if elem.__class__ is Failure:
                        return False
                    if elem.__class__ is Error:
                        return False
                    if elem.__class__ is Skipped:
                        return False
                return True

        return False