import sys
from framework.Experiment import Experiment
from injectable import load_injection_container

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Use: python py/CloneProject.py <project_name> <issueId>")
        exit()

    load_injection_container()

    projectName = sys.argv[1]
    bugId = str(sys.argv[2])

    experiment = Experiment(projectName, bugId)

    # IF PROJECT DOES NOT EXIST -> CLONE
    experiment.project.clone()