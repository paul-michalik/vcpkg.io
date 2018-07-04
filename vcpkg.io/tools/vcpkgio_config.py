import os,platform,sys,yaml
from os import path

class vcpkgio_config:
    def __init__(self,setting):
        self._setting = setting
    
    def get_remote_setting(self,key=None):
        if key:
            return self._setting['remote_setting'][key]
        return self._setting['remote_setting']

    def get_binary_setting(self,key=None):
        if key:
            return self._setting['binary_setting'][key]
        return self._setting['binary_setting']

    def get_vcpkg_setting(self,key=None):
        if key:
            return self._setting['vcpkg_setting'][key]
        return self._setting['vcpkg_setting']

    def get_download_setting(self,key=None):
        if key:
            return self._setting['download_setting'][key]
        return self._setting['download_setting']

    def get_action(self):
        return self._setting['action']

    def get_setting(self):
        return self._setting
    def get_setting_str(self,key,prefix="",infix="",postfix=""):
        conan_setting_frmt =  prefix+infix.join(str(setting_type)+postfix for setting_type in self._setting[key].keys())
        value_list = [setting_val[0] for setting_val in self._setting[key].values()]
        default_setting_value =  conan_setting_frmt.format(*value_list)
        return default_setting_value

    def set_remote_setting(self,key,val):
        self._setting['remote_setting'][key] = val
    def set_binary_setting(self,key,val):
        self._setting['binary_setting'][key] = val
    def set_vcpkg_setting(self,key,val):
        self._setting['vcpkg_setting'][key] = val
    def get_remote_status(self):
        status = False
        if 'username' in self._setting['remote_setting'].keys() and "password" in self._setting['remote_setting'].keys():
            status = True
        return status