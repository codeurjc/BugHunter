# git show -s --format=%ci <mytagname>^{commit}
from github import Github
import re
import sys
import json
import datetime
from jira import JIRA
import urllib.request, json 
import requests
from bs4 import BeautifulSoup

from py.framework.Bug import Bug
from py.framework.utils.GitUtils import GitManager

def parseDateJira(date:str):
    return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d %H:%M:%S %z')

def parseDateSourceforge(date:str):
    return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S %z') + "+0000"

def parseDateFromTimestamp(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S %z')) + "+0000"

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
        regex = r"https:\/\/issues.apache.org\/(.*)\/browse\/(.*)"
        m = re.search(regex, report_path)
        if m is None: exit(1)
        issue_id = m.group(2)

        jira = JIRA('https://issues.apache.org/jira/')
        jira_issue = jira.issue(issue_id)
        bug.bugConfig['issue_created_at'] = parseDateJira(jira_issue.fields.created)
        bug.bugConfig['issue_closed_at'] = parseDateJira(jira_issue.fields.resolutiondate)
    elif "storage.googleapis.com" in report_path:
        with urllib.request.urlopen(report_path) as url:
            data = json.loads(url.read().decode())
            bug.bugConfig['issue_created_at'] = parseDateFromTimestamp(data['comments'][0]['timestamp'])
            bug.bugConfig['issue_closed_at'] =parseDateFromTimestamp(data['comments'][-1]['timestamp'])
    elif "sourceforge.net" in report_path:
        with urllib.request.urlopen(report_path) as url:
            html = url.read().decode()
            soup = BeautifulSoup(html, 'html.parser')
            created = soup.find(string="Created:").find_next('span').getText().strip()
            updated = soup.find(string="Updated:").find_next('span').find('span').getText().strip()
            bug.bugConfig['issue_created_at'] = parseDateSourceforge(created)
            bug.bugConfig['issue_closed_at'] = parseDateSourceforge(updated)
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