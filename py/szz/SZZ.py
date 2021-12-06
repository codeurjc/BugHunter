import warnings

from injectable import Autowired, autowired
from py.framework.Bug import Bug
from py.framework.Project import Project
from py.framework.utils.DockerUtils import DockerClient
from py.framework.utils.utils import createDirIfNotExist

warnings.filterwarnings("ignore")

WORKDIR="/home/regseek/workdir"

class SZZ():

    @autowired
    def __init__(self, project_name, bugId, algName, dockerClient: Autowired(DockerClient)):
        self.experiment_id = project_name + "_Bug_" + bugId + "_" + algName
        self.bug = Bug(project_name, bugId)
        self.dockerClient = dockerClient
        self.project = Project(project_name, self.experiment_id, self.bug)
        self.project.clone()
        # Create results folder
        self.results_dir = WORKDIR+"/results/szz/"+algName+"/"+self.experiment_id+"/"
        self.log_path = self.results_dir + algName + ".log"
        createDirIfNotExist(self.results_dir)

    def execute(self): 
        pass
