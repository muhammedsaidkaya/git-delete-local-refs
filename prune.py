from sh import git
import os

def get_branch_names(exceptList=[], remote=False):
        # Prepare script which gets all branches on remote repository
        # except for items on the exceptList
        script = "git branch " + ("-r" if remote else "")
        for branchName in exceptList:
            script += " | awk '! /{}/' ".format(branchName)
        # Get all branchname
        result = (os.popen(script).read()).split("\n")
        result.pop()
        result = list(map(lambda x: x.lstrip(), result))
        if remote:
            result = list(map(lambda x: x.replace("origin/",""), result))
        return result

def get_untrackked_refs(remote_branches=[], local_branches=[]):
    remote_branches = set(remote_branches)
    local_branches = set(local_branches)
    return local_branches - remote_branches

def delete_branches(branches):
    for branch in branches:
        git.branch("-D", branch)

remote_branches=get_branch_names(["master", "release/6.4"], remote=True)
local_branches=get_branch_names(["master", "release/6.4"], remote=False)
refs=get_untrackked_refs(remote_branches, local_branches)
delete_branches(refs)