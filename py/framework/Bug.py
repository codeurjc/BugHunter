import json

class Bug():
    
    def __init__(self, project, bugId):
        with open('configFiles/{project}/bugs/Bug-{bugId}.json'.format(project=project, bugId=bugId)) as f:
            self.bugConfig = json.load(f)
        self.id = bugId
        self.fixCommit = self.bugConfig['fix_commit']
        self.testPath = self.bugConfig['folder'] + self.bugConfig['file']
        self.testFolder = self.bugConfig['folder']
        self.testFile = self.bugConfig['file']

        self.build_source_command = self.bugConfig['build']
        self.build_test_command = self.bugConfig['build_test']
        self.test_command = self.bugConfig['test_command']
        self.test_report = self.bugConfig['test_report']