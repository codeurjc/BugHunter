from framework.utils.DockerUtils import DockerClient
from injectable import Autowired, autowired, injectable
import csv
import json
import re
import os
import sys

@injectable(singleton=True)
class Defects4J():

    @autowired
    def __init__(self, dockerClient: Autowired(DockerClient)):
        self.dockerClient = dockerClient
        self.container_name = "d4j-container"
        self.dockerClient.initContainer("defects4j:2.0.0", "d4j-container", reuse=True)

    def cloneRepository(self, projectName, experimentId):
        projectFolder = "/home/regseek/workdir/projects/{experimentId}".format(experimentId= experimentId)
        cmd = "defects4j checkout -p {projectName} -v 1b -w {projectFolder} && chmod -R 777 {projectFolder}".format(projectName=projectName, projectFolder=projectFolder)
        return self.dockerClient.execute(self.container_name, cmd)

    def getAllBugs(self, projectName):
        cmd = "cat /defects4j/framework/projects/{projectName}/active-bugs.csv".format(projectName=projectName)
        exit_code, container_output = self.dockerClient.execute(self.container_name, cmd)

        lines = container_output.decode("utf-8") .splitlines()
        reader = csv.reader(lines)
        headers = next(reader)
        bugs = [{h:x for (h,x) in zip(headers,row)} for row in reader]
        
        return bugs

    def generateBugConfigFile(self, projectConfig, bug):
        cmd = "defects4j info -p {projectName} -b {bugId}".format(projectName=projectConfig['project'], bugId=bug['bug.id'])
        exit_code, container_output = self.dockerClient.execute(self.container_name, cmd)
        
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
            "git_url": projectConfig['git_url'],
            "docker_image": projectConfig['docker_image'],
            "bug_report": bug['report.url'],
            "fix_commit": fix_commit,
            "build": projectConfig['build'],
            "build_test": projectConfig['build_test'],
            "test_command": test_command,
            "folder":  test_folder,
            "file": test_file,
            "test_report" : report_path,
        }
        

        if not os.path.isdir("configFiles/%s/bugs/" % (projectConfig['project'])):
            os.makedirs("configFiles/%s/bugs/" % (projectConfig['project']))
        
        with open('configFiles/%s/bugs/Bug-%s.json' % (projectConfig['project'], bug['bug.id']), 'w+') as fp:
            json.dump(configFile, fp, indent=4)