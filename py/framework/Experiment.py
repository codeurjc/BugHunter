import os
from datetime import datetime
import shutil
from injectable import Autowired, autowired

from framework.utils.ProcessUtils import ProcessManager
from framework.utils.DockerUtils import DockerClient
from framework.Bug import Bug
from framework.Project import Project
from framework.utils.utils import createDirIfNotExist


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

        #self.dockerClient.createVolumeIfNotExist(self.id)

    def initProjectContainer(self):
        m2_path=os.getcwd()+"/"+self.bug_folder+"libs/"
        
        env = {
            "M2_FOLDER": m2_path
        }
        self.dockerClient.initContainer(
            self.project.dockerImage, 
            self.id, 
            workdir=self.project.path,
            env=env
        )
    
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