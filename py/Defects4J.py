from DockerUtils import DockerClient
import csv
import json
import re
import os
import sys

class Defects4J():

    def __init__(self, container_name="defects4j-container"):
        self.dockerUtils = DockerClient()
        self.container_name = container_name

    def cloneRepository(self, projectName):
        cmd = "defects4j checkout -p {projectName} -v 1b -w /tmp/{projectName}/".format(projectName=projectName)
        os.mkdir('/home/regseek/workdir/{projectName}/'.format(projectName=projectName))
        volumes = ['/home/regseek/workdir/{projectName}/:/tmp/{projectName}/'.format(projectName=projectName)]
        return self.dockerUtils.execute("defects4j:2.0.0", self.container_name, cmd, volumes=volumes)

    def getAllBugs(self, projectName):
        cmd = "cat /defects4j/framework/projects/{projectName}/active-bugs.csv".format(projectName=projectName)
        exit_code, container_output = self.dockerUtils.execute("defects4j:2.0.0", self.container_name, cmd)

        lines = container_output.decode("utf-8") .splitlines()
        reader = csv.reader(lines)
        headers = next(reader)
        bugs = [{h:x for (h,x) in zip(headers,row)} for row in reader]
        
        return bugs

    def generateBugConfigFile(self, projectConfig, bug):
        cmd = "defects4j info -p {projectName} -b {bugId}".format(projectName=projectConfig['project'], bugId=bug['bug.id'])
        exit_code, container_output = self.dockerUtils.execute("defects4j:2.0.0", self.container_name, cmd)
        
        text = container_output.decode("utf-8") 

        # fix_commit = re.search(r"Revision ID \(fixed version\):\n(.*)", text).group(1)
        fix_commit = bug['revision.id.fixed']

        matches = re.search(r"Root cause in triggering tests:\n\s+-\s+(.*)\n\s+-->\s+(.*)", text)
        
        test_info = matches.group(1)
        test_command = projectConfig['test_command']%test_info.replace('::','#')
        test_path = projectConfig['test_path'] % test_info.split('::')[0].replace('.','/')
        test_file= test_path.split('/')[-1]
        test_folder= "/".join(test_path.split('/')[:-1]) + "/"
        report_path= projectConfig['report_path'] % test_info.split('::')[0]


        configFile = {
            "id": bug['bug.id'],
            "project": projectConfig['project'],
            "bug_report": bug['report.url'],
            "fix_commit": fix_commit,
            "build": projectConfig['build'],
            "folder":  test_folder,
            "file": test_file,
            "test_command": test_command,
            "test_report" : report_path,
        }
        

        if not os.path.isdir("configFiles/%s/bugs/" % (projectConfig['project'])):
            os.makedirs("configFiles/%s/bugs/" % (projectConfig['project']))
        
        with open('configFiles/%s/bugs/Bug-%s.json' % (projectConfig['project'], bug['bug.id']), 'w+') as fp:
            json.dump(configFile, fp, indent=4)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Use: python py/Defects4J.py <d4j_project_name>")
        exit()

    with open('configFiles/{project}/project-config.json'.format(project=sys.argv[1])) as f:
        projectConfig = json.load(f)

    d4j = Defects4J()
    d4j.cloneRepository(projectConfig['project'])
    # bug_1 = d4j.getAllBugs(projectConfig['project'])[0]
    # d4j.generateBugConfigFile(projectConfig, bug_1)