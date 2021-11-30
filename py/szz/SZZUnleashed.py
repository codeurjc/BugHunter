import sys
import json
from injectable import load_injection_container

from py.framework.Bug import Bug
from py.framework.Project import Project
from py.framework.utils.utils import createDirIfNotExist

WORKDIR="/home/regseek/workdir"

def executeSZZUnleashed(project_name, bugId): 

    experiment_id = project_name + "_Bug_" + bugId + "_SZZUnleashed"
    bug = Bug(project_name, bugId)
    project = Project(project_name, experiment_id, bug)
    project.clone()

    # Create results folder
    results_dir = WORKDIR+"/results/szz/SZZUnleashed/"+experiment_id+"/"
    log_path = results_dir + "SZZUnleashed.log"
    createDirIfNotExist(results_dir)

    # Generate and save Issue info
    issue = {}
    issue[experiment_id] = {
        "creationdate": bug.bugConfig['issue_created_at'],
        "resolutiondate": bug.bugConfig['issue_closed_at'],
        "hash": bug.fixCommit,
        "commitdate":bug.bugConfig['fix_date']
    }

    with open(results_dir+"issue.json",'w+') as json_file:
        json.dump(issue, json_file, indent=4)

    # Launch container with SZZ
    
    project.dockerClient.initContainer("szz-unleashed:0.1.0", experiment_id, workdir=results_dir)

    issue_path = results_dir+"/issue.json"
    project_path = WORKDIR+"/projects/"+experiment_id
    _, log = project.dockerClient.execute(experiment_id, "java -jar /home/szz/szz.jar -i {issue_path} -r {project_path}".format(issue_path=issue_path, project_path=project_path), withTimeout=False)

    with open(log_path, "wb+") as out:
        out.write(log)

    project.dockerClient.shutdownContainers()

if __name__ == "__main__":

    load_injection_container(search_path="/home/regseek/workdir/py")

    if len(sys.argv) < 3:
        print("Use: python py/szz/SZZUnleashed.py <project_name> <bugId>")
        exit()

    rs = executeSZZUnleashed(sys.argv[1], str(sys.argv[2]))
