from GitUtils import GitManager
from utils import createDirIfNotExist
from structure import Bug, Project, Experiment

import os
import sys
import json
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

        # 1) CHECK FIX COMMIT
        self.experiment.log("Checking FIX COMMIT: %s"%fix_commit['hash'])
        self.checkCommit(fix_commit)
        
        # 2) CHECK PREVIOUS COMMIT (ASSERT NO FLAKY TEST)
        self.experiment.log("Checking PREVIOUS COMMIT: %s"%previous_commit['hash'])
        self.experiment.applyRegressionTest()
        self.checkCommit(previous_commit)

        # 3) CHECK ALL PREVIOUS COMMITS
        self.experiment.log("Checking ALL PREVIOUS COMMITS")

        # self.experiment.log(" -> Checking commit %s"%commit['hash'])

    def checkCommit(self, commit):

        commitResultsPath = "{commitsFolder}/{id}-{hash}/".format(commitsFolder=self.experiment.commits_folder, id=commit['id'], hash=commit['hash'])
        
        created = createDirIfNotExist(commitResultsPath)

        if not created:
            self.experiment.log("Commit already checked", log_prefix=commit['hash'][0:17])
            return

        # 1) Checkout commit
        self.gitManager.change_commit(commit['hash'])

        # 2) Build source
        isSuccess = self.experiment.project.buildSource(commitResultsPath)
        if not isSuccess: return

        # 3) Build test
        isSuccess = self.experiment.project.buildTests(commitResultsPath)
        if not isSuccess: return

        # 4) Run test
        isSuccess = self.experiment.project.executeTest(commitResultsPath)
        if not isSuccess: return

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



    