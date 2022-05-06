import os
import json
import re
import sys
from shutil import copy
from CommitGraph import CommitGraph

sys.setrecursionlimit(20000) # Current limit = 999

class Analysis:

    def __init__(self, root="/home/jovyan/work"):
        self.root=root
        self.analysis_results_path = self.root + "/analysis/results/"
        createDirIfNotExists(self.analysis_results_path)

    def getTestName(self, cmd):
    
        if cmd.startswith("mvn"):
            return re.search(r"-Dtest=(.*) test",cmd).group(1)
        if cmd.startswith("ant"):
            return re.search(r"-Dtest.entry.method=(.*) run",cmd).group(1)

    def analyzeBug(self,project, bug_id, force=False):
        
        bug_name = "Bug_"+str(bug_id)
        bug_path = "{root}/results/{project}/{bug_name}/".format(root=self.root, project=project, bug_name=bug_name)
        results_dir = self.analysis_results_path+"{project}/{bug_name}/".format(project=project, bug_name=bug_name)
        result_file = results_dir+"bug_result.json"
        
        
        if not force and os.path.isfile(result_file):  
            with open(result_file) as json_file:
                bug_result = json.load(json_file)  
                return bug_result
        
    #     print("INIT "+project+" "+bug_name)
        
        with open("{root}/configFiles/{project}/bugs/{bug_name}.json".format(root=self.root,project=project, bug_name=bug_name)) as f:
            bug_info = json.load(f)
            
        test_name = self.getTestName(bug_info['test_command'])
        #test_method = test_name.split("#")[1]

        bug_result = {
            'id': project + "_" + bug_name,
            'bug': bug_name,
            'project': project,
            "fix_pass": True,
            "prev_fails": True,
            "category": None,
            "sub_category": "-",
            "test_name": test_name,
            "bug_report": bug_info['bug_report'],
            "fix_commit": bug_info['fix_commit'],
            "BIC_candidates": []
        }
        
        if not os.path.isfile(bug_path+'commit_history.csv'):
            bug_result['category'] = "Other error"
            return bug_result
        
        createDirIfNotExists(results_dir)
        
        try:
            commit_graph = CommitGraph(project, bug_id, bug_path, results_dir, restore=True)
        except IndexError as e:
            bug_result['category'] = "No results - Error at performing experiment"
            return bug_result
            
        fix_commit = commit_graph.graph[bug_info['fix_commit']]
        
        if not fix_commit['ExecuteTest']: # FIX COMMIT - SHOULD PASS
            
            bug_result['category'] = "Test fails in the fix commit"
            bug_result['fix_pass'] = False
            bug_result['prev_fails'] = None
            
            if fix_commit['Build']:
                if fix_commit['BuildTest']:
                    if not fix_commit['HasTestReport']:
                        bug_result['sub_category'] = "The test was not executed"
                    else:
                        bug_result['sub_category'] = "Test execution fails"
                else:
                    bug_result['sub_category'] = "Failure in test build"
            else:
                bug_result['sub_category'] = "Failure in source build"
            
            bug_result['executionsOnPastSequentially'] = 0
        
        else: 

            # SEARCH REGRESSION
            candidates = self.searchRegression(commit_graph.graph, fix_commit)
            if len(candidates) > 0:

                bug_result['BIC_candidates'] = list(map(lambda c: (c['id'],c['commit'] ),candidates))
                bug_result['category'] = "A regression is detected"

                if len(candidates) == 1:
                    bug_result['sub_category'] = "Unique candidates" 
                    
                    # Copy test report 
                    test_report_path = bug_path+"commits/{id}-{commit_hash}/test-report.xml".format(
                        id=candidates[0]['id'],
                        commit_hash=candidates[0]['commit']
                    )
                    copy(test_report_path, results_dir+"bic-test-report.xml")
                else:
                    bug_result['sub_category'] = "Multiple candidates" 

            # SEARCH OTHER BIC
            else:
                bug_result['category'] = "No regression is detected"
                bug_result['sub_category'] = "-"

        executionsOnPast = 0
        buildFailCount = 0
        buildTestFailCount = 0
        
        for node in commit_graph.graph.values():
            if node['HasTestReport']: executionsOnPast+=1
            if node['State'] == 'TestBuildError': buildFailCount +=1
            if node['State'] == 'BuildError': buildTestFailCount += 1
                
        bug_result['executionsOnPast'] = executionsOnPast
        bug_result['buildFail'] = buildFailCount
        bug_result['buildTestFail'] = buildTestFailCount
        bug_result['numCommits'] = len(commit_graph.graph.values())
        
        # Save bug result
        with open(results_dir+"bug_result.json",'w+') as json_file:
            json.dump(bug_result, json_file, indent=4)

        return bug_result

    def searchRegression(self, graph, init_node):
        candidates = []
        visited = []
        queue = []
        candidate_path = []

        queue.append(init_node)

        while queue:
            node = queue.pop()  

            successParents = True
            parents = graph[node['commit']]['parents']

            if node['State'] == "TestFail":
                candidates = []

            for parent_hash in parents:
                if parent_hash not in graph: # Reach first commit
                    successParents = False
                    if len(queue)==0:
                        break
                    else: 
                        continue # Check other branches
                parent = graph[parent_hash]
                successParent = parent['State'] == "TestSuccess"
                successParents = successParents and successParent
                if not successParent:
                    if parent['State'] in ["BuildError", "TestBuildError"]:
                        candidates.append(node)
                    if parent_hash not in visited:
                        visited.append(parent_hash)
                        queue.append(parent)
        
            if successParents and node['State'] != "TestSuccess":
                
                if node['State'] == 'TestFail': 
                    return [node]
                else:
                    candidates = candidates + [node]
                    if len(queue)==0:
                        return candidates
                    else:
                        candidate_path = candidates
        
        return candidate_path

def createDirIfNotExists(folder_name):
    if not os.path.isdir(folder_name): 
        os.makedirs(folder_name)