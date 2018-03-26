import os,platform,sys,yaml
from tools.conan import conan_tools

class remote_tools(object): 
    def factory(setting):
        if 'conan' == setting['remote_setting']['remote_client']:
            return conan_tools.conan_tools(setting)
 
    factory = staticmethod(factory)