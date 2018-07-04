import os,platform,sys,yaml
from os import path
from tools.conan import conan_service
from tools import system_tools,vcpkgio_config
from conans import tools

class conan_tools:
    def __init__(self,setting):
        self._conan_root = os.path.dirname(os.path.abspath(__file__))
        self._setting = vcpkgio_config.vcpkgio_config(setting) 
        self._conan = conan_service.conan(setting)

    '''
    configure conan package
        - remove unnecessary files
        - uncompress download file 
        - delete compressed download file
    '''
    def _configure_conan_pkg(self,download_folder):
        ret_code = 0
        system_tools.remove(download_folder,".txt")
        bin_files = system_tools.count_subparts(download_folder,self._setting.get_binary_setting('bundle_name')[0])
        if len(bin_files): 
            system_tools.uncompress(bin_files[0] , download_folder)   
            system_tools.remove(download_folder,'.7z' )
        else:
            ret_code = 1      
        return ret_code

    def download_bin(self,download_folder):
        print("downloading please wait...")
        self._conan._conan_download(download_folder)
        ret_code=self._configure_conan_pkg(download_folder)        
        if not ret_code:
            ret_code = True
            print("downloading completed successfully and check %s" % download_folder)
        else:
            ret_code = False
            print("downloading failed !!!")
        return ret_code


    def upload_bin(self,bin_folder):        
        if self._setting.get_remote_status():
            print("split and compressing please wait...")
            bin_files = system_tools.compress_bin(bin_folder,self._setting.get_binary_setting('bundle_name')[0])
            print("uploading please wait...")
            if len(bin_files):                
                for index in range(0,len(bin_files)):
                    self._conan._conan_upload(bin_folder,bin_files[index],index)
                print("uploading completed successfully...")
                system_tools.remove(bin_folder,'.7z')
            else:
                print("uploading failed!! and check %s" % bin_folder)
        else:
            print("remote user name and password is not set !!!")