from framework.utils.GitUtils import GitManager
from framework.Experiment import Experiment
from framework.utils.utils import createDirIfNotExist
import warnings
warnings.filterwarnings("ignore")

import sys
import traceback
import json
import os
from injectable import load_injection_container

class RegTestExecutor():

    def __init__(self, projectName, bugId):

        self.experiment = Experiment(projectName, bugId)

        # IF PROJECT DOES NOT EXIST -> CLONE
        self.experiment.project.clone()
        
        self.gitManager = GitManager(self.experiment.project.path, self.experiment.bug.fixCommit)
    
    def execute(self):

        # Init container with project

        allCommits = self.gitManager.generateCommitList(self.experiment.bug_folder+"commit_history.csv")

        fix_commit = allCommits[0]
        previous_commits = allCommits[1:]

        # 0) GET REGRESSION TEST
        self.gitManager.change_commit(fix_commit['hash'])
        self.experiment.initProjectContainer()
        self.experiment.project.applyFixes(self.experiment.bug_folder+ "apply-fixes-before-all.log") # In case of need to move to subfolder
        self.experiment.saveRegressionTest()

        # 1) CHECK FIX COMMIT
        self.experiment.log("Checking FIX COMMIT: %s"%fix_commit['hash'])
        fix_result = self.checkCommit(fix_commit)
        if not fix_result['isTestExecutionSuccess']:
            self.experiment.log("Test fail on fix commit: Abort experiment")
            return

        # 2) CHECK ALL PREVIOUS COMMITS
        self.experiment.log("Checking ALL PREVIOUS COMMITS")

        for commit in previous_commits:
            self.experiment.log("Checking commit {c_id}-{c_hash}".format(c_id=commit['id'], c_hash=commit['hash']))
            self.checkCommit(commit)

    def checkCommit(self, commit):

        commitResultsPath = "{commitsFolder}/{id}-{hash}/".format(commitsFolder=self.experiment.commits_folder, id=commit['id'], hash=commit['hash'])
        
        createDirIfNotExist(commitResultsPath)

        if os.path.exists(commitResultsPath+"result.json"):
            self.experiment.log("Commit already checked", log_prefix=commit['hash'][0:17])
            with open(commitResultsPath+"result.json") as f:
                return json.load(f)     
        
        # 1) Checkout commit
        self.gitManager.change_commit(commit['hash'])

        # 2) Apply regression test and fixes
        self.experiment.project.applyFixes(commitResultsPath+ "apply-fixes.log")
        self.experiment.applyRegressionTest()

        # 3) Build source
        isSourceBuildSuccess = self.experiment.project.buildSource(commitResultsPath)
        isTestBuildSuccess     = False
        isTestExecutionSuccess = False

        # 4) Build test
        if isSourceBuildSuccess:
            isTestBuildSuccess = self.experiment.project.buildTests(commitResultsPath)
            if isTestBuildSuccess:
                # 5) Run test
                isTestExecutionSuccess = self.experiment.project.executeTest(commitResultsPath)
                if not isTestExecutionSuccess:
                    # Since it is possible that multiple tests are executed 
                    # (the filtering has not worked, usually due to limitations 
                    # of the test library), it is necessary to check that the test 
                    # that detects the failure is the one that passes or fails.
                    isTestExecutionSuccess = self.experiment.project.getTestReportResult(commitResultsPath)

        # 6) Save results
        with open(commitResultsPath+"result.json",'w+') as json_file:
            result = {
                "isSourceBuildSuccess" : isSourceBuildSuccess,
                "isTestBuildSuccess" : isTestBuildSuccess,
                "isTestExecutionSuccess" : isTestExecutionSuccess
            }
            json.dump(result, json_file, indent=4)
        
        return result
            
    def finish(self, message):
        self.experiment.close(message)


if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("Use: python py/RegTestExecutor.py <project_name> <bugId>")
        exit()

    load_injection_container()

    rs = RegTestExecutor(sys.argv[1], str(sys.argv[2]))

    try:
        rs.execute()
    except KeyboardInterrupt as e:
        rs.finish("FINISHED EXPERIMENT WITH KeyboardInterrupt")
    except Exception as e:
        _, msg, _ = sys.exc_info()
        tb = traceback.format_exc()
        print(tb)
        rs.finish("FINISHED EXPERIMENT WITH AN EXCEPTION: %s\n %s"%(msg, tb))
    else:
        rs.finish("EXPERIMENT FINISHED SUCCESSFULLY")



    