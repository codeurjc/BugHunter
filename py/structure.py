import json
import os
from datetime import datetime
import shutil
from injectable import Autowired, autowired

from Defects4J import Defects4J
from GitUtils import GitManager, cloneRepository
from utils import createDirIfNotExist
from ProcessUtils import ProcessManager
from DockerUtils import DockerClient

class Experiment():

    @autowired
    def __init__(self, projectName, bugId, dockerClient: Autowired(DockerClient), processManager:Autowired(ProcessManager)):

        self.id = projectName +"_Bug_"+bugId

        self.bug = Bug(projectName, bugId)
        self.project = Project(projectName, self.id, self.bug)

        # CREATE RESULTS FOLDER IF NOT EXIST
        project_results_folder = "results/%s" % (projectName)
        createDirIfNotExist(project_results_folder+"/ExperimentLogsLogs/")

        # CREATE BUG FOLDER IF NOT EXIST
        self.bug_folder = "results/%s/Bug_%s/" % (projectName, bugId)
        self.commits_folder = self.bug_folder+"commits/"
        createDirIfNotExist(self.commits_folder)

        # CREATE PROCESS MANAGER AND GENERAL LOGS FOLDER
        general_logs_folder = project_results_folder+"/ExperimentLogsLogs/Bug_"+bugId+"/"
        createDirIfNotExist(general_logs_folder)
        date = datetime.now().strftime('%Y%m%d%H%M%S')
        self.pm = processManager
        self.pm.setNewOutput(general_logs_folder+"Bug_"+bugId+"_"+date+".log", "REGRESSION SEEKER")

        self.dockerClient = dockerClient
    
    def saveRegressionTest(self):
        shutil.copyfile(self.project.path+self.bug.testPath, self.bug_folder + self.bug.testFile)

    def applyRegressionTest(self):
        createDirIfNotExist(self.project.path+self.bug.testFolder)
        shutil.copyfile(self.bug_folder + self.bug.testFile,self.project.path+self.bug.testPath)

    def log(self, msg, log_prefix=None):
        self.pm.log(msg, log_prefix=log_prefix)

    def close(self, msg):
        self.dockerClient.shutdownContainers()
        self.log(msg)
        self.pm.close()

class Project():

    @autowired
    def __init__(self, projectName, experimentId, bug, dockerClient: Autowired(DockerClient), processManager:Autowired(ProcessManager)):
        
        with open('configFiles/{project}/project-config.json'.format(project=projectName)) as f:
            self.projectConfig = json.load(f)

        self.name = projectName
        self.bug = bug
        self.experimentId = experimentId
        self.repository = self.projectConfig['git_url']
        self.path = "{cwd}/projects/{experimentId}/".format(cwd=os.getcwd(), experimentId=self.experimentId)
        self.pm = processManager
        self.dockerClient = dockerClient

    def clone(self):
        if not os.path.isdir(self.path):
            if self.repository == "D4J":
                d4j = Defects4J()
                d4j.cloneRepository(self.name, self.experimentId)
            else:
                cloneRepository(self.repository,self.path)

    def buildSource(self, resultsPath): 
        return self.executeOnCommit(self.bug.build_source_command , resultsPath + "source-build.log")

    def buildTests(self, resultsPath):
        return self.executeOnCommit(self.bug.build_test_command, resultsPath + "test-build.log")

    def executeTest(self, resultsPath):
        isSuccess = self.executeOnCommit(self.bug.test_command, resultsPath + "test-execution.log")
        shutil.copyfile(self.path+self.bug.test_report, resultsPath + "test-report.xml")
        return isSuccess

    def executeOnCommit(self, cmd, log_path):
    
        exit_code, log = self.dockerClient.execute(
            self.projectConfig['docker_image'], 
            self.experimentId, 
            cmd, 
            workdir=self.path
        )

        with open(log_path, "wb+") as out:
            out.write(log)

        isSuccess = exit_code == 0
        
        if isSuccess:
            self.pm.log("   %s SUCCESS"%cmd)
        else:
            self.pm.log("   %s FAILS"%cmd)
        
        return isSuccess
        

class Bug():

    def __init__(self, project, bugId):
        with open('configFiles/{project}/bugs/Bug-{bugId}.json'.format(project=project, bugId=bugId)) as f:
            self.bugConfig = json.load(f)
        self.fixCommit = self.bugConfig['fix_commit']
        self.testPath = self.bugConfig['folder'] + self.bugConfig['file']
        self.testFolder = self.bugConfig['folder']
        self.testFile = self.bugConfig['file']

        self.build_source_command = self.bugConfig['build']
        self.build_test_command = self.bugConfig['build_test']
        self.test_command = self.bugConfig['test_command']
        self.test_report = self.bugConfig['test_report']
