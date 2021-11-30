# git show -s --format=%ci <mytagname>^{commit}
from github import Github

def getIssue(self):
    g = Github()
    repo = g.get_repo("JodaOrg/joda-time")
    gh_issue = repo.get_issue(number=93)
    print(dir(gh_issue))
    print(gh_issue.closed_at)
    print(gh_issue.created_at)
    return gh_issue