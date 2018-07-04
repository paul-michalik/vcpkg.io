import os,platform,sys,time,yaml
from colorama import init,Fore
from conans import ConanFile,tools

class git_tools:
    def __init__(self,cur_path):
        self.working_dir = cur_path
        self._git_cmd ={}
        self._git_cmd["clone"] = "git clone --recursive %s %s"
        self._git_cmd["pull"] = "cd %s && git pull && vcpkg upgrade --no-dry-run"
        self._git_cmd["download"] = "cd %s && git fetch origin %s && git checkout FETCH_HEAD"


    '''
        run git command
    '''
    def _run_git_cmd(self,command,tup=()):
        git_cmd = self._git_cmd[command]        
        if len(tup):
            git_cmd = self._git_cmd[command] % (tup) 
        ret_code = os.system(git_cmd)
        return ret_code

    '''
        get git interface
    '''
    def get_git_cmd(self):
        git_tools_api ={}        
        git_tools_api["clone"]=self.clone
        git_tools_api["pull"]=self.pull
        git_tools_api["download"]=self.download
        return git_tools_api

    def clone(self,url="https://github.com/Microsoft/vcpkg.git",directory=None):
        if not directory:
            directory = self.working_dir+os.sep+"vcpkg"
        return self._run_git_cmd("clone",(url,directory))

    def pull(self,directory=None):
        if not directory:
            directory = self.working_dir+os.sep+"vcpkg"
        return self._run_git_cmd("pull",(directory))

    def download(self,directory=None,url="https://github.com/Microsoft/vcpkg.git",VcPkgCommit="15e4f46b45c432a41ee6a962609039bc2497ec19"):
        if not directory:
            directory = self.working_dir+os.sep+VcPkgCommit
        else:
            directory=directory+os.sep+VcPkgCommit
        self.clone(url,directory)
        self._run_git_cmd("download",(directory,VcPkgCommit))
        return self.working_dir+os.sep+VcPkgCommit
