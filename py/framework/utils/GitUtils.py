import os
import csv
import git

DELIMITER="|=|"

def cloneRepository(url, dest):
    git.Repo.clone_from(url, dest)

class GitManager:

    HEADERS = ["id", "hash", "date", "comment"]

    def __init__(self, project_path, base_commit, url=None):
        self.project_path = project_path
        self.base_commit = base_commit
        self.repo = git.Repo(project_path)

    def change_commit(self,commit_hash):
        self.repo.git.clean("-fdx")
        self.repo.git.checkout('-f',commit_hash) 

    def generateCommitList(self, history_file_path):

        if not os.path.isfile(history_file_path):

            # GET COMMITS
            res = self.repo.git.log('--pretty=format:%%H%s%%ad%s%%s'%(DELIMITER, DELIMITER),'--date=iso8601','--reverse', self.base_commit, "--")
            allCommits = list(map(lambda commit_info: commit_info.split(DELIMITER),res.split('\n')))
            allCommits.reverse()

            # SAVE COMMIT HISTORY
            with open(history_file_path, 'w+') as csvfile: 
                writer = csv.DictWriter(csvfile, fieldnames = self.HEADERS) 
                commits = []
                n=0
                for commit in allCommits:
                    commit_hash, date, comment = commit
                    #print(commit)
                    commits.append({
                        "id": n,
                        "hash": commit_hash.strip(),
                        "date": date.strip(),
                        "comment": comment.strip()
                    })
                    n+=1
                writer.writeheader()
                writer.writerows(commits)
            
            return commits

        else:
            # LOAD PREVIOUS COMMITS
            commits = []
            with open(history_file_path) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    commits.append(row)

            return commits 


if __name__ == "__main__":
    gm = GitManager("~/workdir/projects/JacksonDatabind_Bug_1","88f44d87d4c2251d7cf55d9aa9c3452a397ae19b")
    commits = gm.generateCommitList("/home/regseek/workdir/results/JacksonDatabind/Bug_1/commit_history.csv")
