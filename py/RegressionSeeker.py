from framework.utils.GitUtils import GitManager
from framework.Experiment import Experiment
from framework.utils.utils import createDirIfNotExist
import warnings
warnings.filterwarnings("ignore")

import sys
import json
import os
from injectable import load_injection_container

class RegressionSeeker():

    def __init__(self, projectName, bugId):

        self.experiment = Experiment(projectName, bugId)

        # IF PROJECT DOES NOT EXIST -> CLONE
        self.experiment.project.clone()
        
        self.gitManager = GitManager(self.experiment.project.path, self.experiment.bug.fixCommit)
    
    def searchRegression(self):

        # Init container with project

        allCommits = self.gitManager.generateCommitList(self.experiment.bug_folder+"commit_history.csv")

        fix_commit = allCommits[0]
        previous_commit = allCommits[1]
        remain_previous_commits = allCommits[2:]

        # 0) GET REGRESSION TEST
        self.gitManager.change_commit(fix_commit['hash'])
        self.experiment.saveRegressionTest()
        self.experiment.initProjectContainer()

        # 1) CHECK FIX COMMIT
        self.experiment.log("Checking FIX COMMIT: %s"%fix_commit['hash'])
        fix_result = self.checkCommit(fix_commit)
        if not fix_result['isTestExecutionSuccess']:
            self.experiment.log("Test fail on fix commit: Abort experiment")
            return
        
        # 2) CHECK PREVIOUS COMMIT (ASSERT NO FLAKY TEST)
        self.experiment.log("Checking PREVIOUS COMMIT: %s"%previous_commit['hash'])
        prev_result = self.checkCommit(previous_commit)
        if prev_result['isTestExecutionSuccess']:
            self.experiment.log("Test pass on previous commit (flaky test): Abort experiment")
            return

        # 3) CHECK ALL PREVIOUS COMMITS
        self.experiment.log("Checking ALL PREVIOUS COMMITS")

        for commit in remain_previous_commits:
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

        # 2) Apply regression test
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

        # Save results
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
        print("Use: python py/ExperimentLogs.py <project_name> <bugId>")
        exit()

    load_injection_container()

    rs = RegressionSeeker(sys.argv[1], str(sys.argv[2]))

    try:
        rs.searchRegression()
    except KeyboardInterrupt as e:
        rs.finish("FINISHED EXPERIMENT WITH KeyboardInterrupt")
    except Exception as e:
        _, msg, _ = sys.exc_info()
        print(e)
        rs.finish("FINISHED EXPERIMENT WITH AN EXCEPTION: %s"%msg)
    else:
        rs.finish("EXPERIMENT FINISHED SUCCESSFULLY")



    