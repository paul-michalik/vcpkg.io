import os,platform,sys,time,yaml
from tools import vcpkg_tools,git_tools,remote_tools,system_tools,vcpkgio_config
from conans import ConanFile,tools
from os import path

class vcpkg_io:   
    def __init__(self):
        self._cur_path =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
        self.git=self.get_git_tools()

    def get_vcpkg_tools(self,vcpkg_src):
        return vcpkg_tools.vcpkg(vcpkg_src)

    def get_git_tools(self):
        return git_tools.git_tools(self._cur_path)

    def get_remote_tools(self,setting):
        return remote_tools.remote_tools.factory(setting)

    '''
        run git clone,pull,download command
    '''
    def run(self,command,par_list=()):
        if "execute" == command:
            self.execute(*par_list)
        else:
            tools =  self.git.get_git_cmd()   
            tools[command](*par_list)

    '''
    execute settingfile to either download and upload package from server 
    it perform following steps
    1. download vcpkg source
    2. create vcpkg object to execute vcpkg related operation
    3. create remote_client(current conan) to upload and download binaries
    '''
    def execute(self,setting_file):
        status,config_data=system_tools.extract_data(setting_file)
        if status == False:
            raise Exception('fail to %s' % setting_file)
        setting = vcpkgio_config.vcpkgio_config(config_data)                    
        if setting.get_action() == 'upload':    
            vcpkg_path = setting.get_vcpkg_setting('vcpkg_local_path')   
            if not vcpkg_path:              
                vcpkg_path = self.git.download()

            if path.exists(vcpkg_path): 
                vcpkg = self.get_vcpkg_tools(vcpkg_path)
                export_folder = vcpkg.export_pkg(setting.get_vcpkg_setting('package_list'),setting.get_vcpkg_setting('triplet_list'),setting.get_binary_setting('bundle_name')[0])
                if export_folder:
                    conan_client = self.get_remote_tools(setting.get_setting())
                    conan_client.upload_bin(export_folder)
        else:
            conan_client = self.get_remote_tools(setting.get_setting())          
            vcpkg_path = setting.get_download_setting('import_vcpkg_path')
            if vcpkg_path != None:
                download_folder = self._cur_path + os.sep +"download" + os.sep + setting.get_binary_setting('bundle_name')[0]
                status = conan_client.download_bin(download_folder)              
                vcpkg = self.get_vcpkg_tools(vcpkg_path)
                if status:
                    vcpkg.import_pkg(download_folder)
                system_tools.remove(download_folder)
            else:
                status = conan_client.download_bin(setting.get_download_setting('download_binary_path'))
 
    
if __name__ == "__main__":
    vcpkgio=vcpkg_io()
    #vcpkgio.execute(sys.argv[1])
    vcpkgio.run(sys.argv[1],sys.argv[2:])
    
