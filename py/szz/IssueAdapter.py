# git show -s --format=%ci <mytagname>^{commit}
from github import Github
import re
import sys
import json
import datetime
from jira import JIRA

from py.framework.Bug import Bug
from py.framework.utils.GitUtils import GitManager

def parseDateJira(date:str):
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d %H:%M:%S %z')

def updateIssue(project_name, bugId):
    bug = Bug(project_name, bugId)

    report_path = bug.bugConfig['bug_report']

    # GET DATES OF ISSUE

    if "github" in report_path:
        regex = r"https:\/\/github\.com\/(.*)\/issues\/(\d+)"
        m = re.search(regex, report_path)
        if m is None: exit(1)
        repo = m.group(1)
        issue_id = int(m.group(2))

        g = Github()
        gh_issue = g.get_repo(repo).get_issue(number=issue_id)

        bug.bugConfig['issue_created_at'] = str(gh_issue.created_at)+" +0000"
        bug.bugConfig['issue_closed_at'] = str(gh_issue.closed_at)+" +0000"
    elif "apache" in report_path:
        jira = JIRA('https://issues.apache.org/jira/')
        jira_issue = jira.issue("COMPRESS-279")
        bug.bugConfig['issue_created_at'] = parseDateJira(jira_issue.fields.created)
        bug.bugConfig['issue_closed_at'] = parseDateJira(jira_issue.fields.resolutiondate)
    else:
        raise Exception("Get issue info not implemented for %s"%report_path)

    # GET DATE OF FIX COMMIT

    project_path = "projects/{project_name}_Bug_{bugId}/".format(project_name=project_name, bugId=bugId)

    bug.bugConfig['fix_date'] = GitManager(project_path).getCommitDate(bug.fixCommit)

    with open('configFiles/{project}/bugs/Bug_{bugId}.json'.format(project=project_name, bugId=bugId),'w+') as json_file:
        json.dump(bug.bugConfig, json_file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Use: python py/szz/IssueAdapter.py <project_name> <issueId>")
        exit()
    updateIssue(sys.argv[1], str(sys.argv[2]))