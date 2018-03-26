import os,platform,sys,time,yaml,re
from conans import tools
from tools import system_tools
from distutils.dir_util import copy_tree

class vcpkg_pkg:
    def __init__(self,root_path):
        self._vcpkg_root_path = root_path

    def get_path(self,type=""):
        if type == 'info':
            return os.sep+"installed"+os.sep+"vcpkg"+os.sep+"info"
        elif type == 'status':
            return os.sep+"installed"+os.sep+"vcpkg"+os.sep+"status"
        elif type == 'export_status':
            return os.sep+"installed"+os.sep+"vcpkg"+os.sep+"export_status"
        elif type == 'vcpkg_app' and platform.system() == 'Windows':
            return  self._vcpkg_root_path +os.sep +"vcpkg.exe"
        elif type == 'vcpkg_app' and platform.system() == 'Linux':
            return  self._vcpkg_root_path +os.sep +"vcpkg"
        elif type == 'bootstrap' and platform.system() == 'Windows':
            return  self._vcpkg_root_path +os.sep +"bootstrap-vcpkg.bat"
        elif type == 'bootstrap' and platform.system() == 'Linux':
            return  self._vcpkg_root_path +os.sep +"bootstrap-vcpkg.sh"
        elif type == 'export':
            return  self._vcpkg_root_path +os.sep +"export"
        return self._vcpkg_root_path 

    def find_pkg_status(self,search_item,source_list):
        is_matched = False
        for source_item in source_list:
            if str(search_item) == str(source_item):
                is_matched = True
                break
        return is_matched
    
    def match_pkg_status(self,pkg_status_data,port,triplet):
        is_matched = False
        if "Package: "+port in str(pkg_status_data) and "Architecture: "+triplet in str(pkg_status_data) :
            if "not-installed" not in str(pkg_status_data):
                is_matched = True
        return is_matched

    def load_installed_pkg_status(self,vcpkg_status_file):
        pkg_status_list=[]
        pkg_status_data=[]
        for status_data in  tuple(open(vcpkg_status_file, 'r')):
            pkg_status_data.append(status_data)
            if status_data == '\n':
                if "not-installed" not in str(pkg_status_data):
                    pkg_status_list.extend([pkg_status_data])
                pkg_status_data=[]                
        return pkg_status_list

    def get_exported_pkg_status(self,exported_pkg_list,vcpkg_status_file):
        pkg_status_list=self.load_installed_pkg_status(vcpkg_status_file)        
        exported_pkg_status_list=[]
        for exported_pkg in exported_pkg_list :
            port,version,triplet = exported_pkg.split("_")
            exported_pkg_status_list.extend([pkg_status for pkg_status in pkg_status_list if self.match_pkg_status(pkg_status,port,triplet)])
        return exported_pkg_status_list

    def get_exported_pkg(self,export_folder):
        vcpkg_info_path = export_folder + self.get_path('info')
        file_list = [f.split(".list")[0] for f in os.listdir(vcpkg_info_path) if f.endswith(".list")]
        return file_list
 
    def save_exported_pkg_status(self,export_folder):
        vcpkg_status_file = self._vcpkg_root_path + self.get_path('status')
        exported_pkg_list = self.get_exported_pkg(export_folder)        
        exported_pkg_status_list = self.get_exported_pkg_status(exported_pkg_list,vcpkg_status_file)
        status_content = "".join(line for dependant_pkg_status in exported_pkg_status_list for line in dependant_pkg_status)
        exported_status_file = export_folder + self.get_path('export_status')
        tools.save(exported_status_file,status_content)

    def load_exported_pkg_status(self):
        vcpkg_status_file = self._vcpkg_root_path + self.get_path('status')
        exported_status_file = self._vcpkg_root_path + self.get_path('export_status')
        pkg_status_list=self.load_installed_pkg_status(vcpkg_status_file)
        exported_pkg_status_list = [new_item for new_item in self.load_installed_pkg_status(exported_status_file) if self.find_pkg_status(new_item,pkg_status_list) == False]
        pkg_status_list.extend(exported_pkg_status_list)
        status_content = "".join(line for pkg_status in pkg_status_list for line in pkg_status)        
        tools.save(vcpkg_status_file,status_content)

class vcpkg:
    def __init__(self,root_path):        
        self._vcpkg_root_path = root_path
        self._vcpkg_pkg = vcpkg_pkg(root_path)
        self._vcpkg_app = self._vcpkg_pkg.get_path('vcpkg_app')
        self._vcpkg_cmd ={}
        self._vcpkg_cmd["export"] = self._vcpkg_app + r" export %s --raw --output=export/%s"
        self._vcpkg_cmd["install"] = self._vcpkg_app +" install %s"
        if os.path.isfile(self._vcpkg_app) == False:
            system_tools.run(self._vcpkg_pkg.get_path('bootstrap'))

    '''
        run vcpkg command
    '''
    def _run_vcpkg_cmd(self,command,tup=()):
        conan_cmd = self._vcpkg_cmd[command]        
        if len(tup):
            conan_cmd = self._vcpkg_cmd[command] % (tup)     
        ret_code = system_tools.run (conan_cmd,False)
        return ret_code

    def export_pkg(self,port_list,triplet_list,bundle_name):
        export_folder = self._vcpkg_pkg.get_path('export') + os.sep + bundle_name
        packages = " ".join([str(port)+":"+str(triplet) for triplet in triplet_list for port in port_list])     
        self._run_vcpkg_cmd("install",(packages))  
        ret_code = self._run_vcpkg_cmd("export",(packages,bundle_name))
        if ret_code == 0:
            self._vcpkg_pkg.save_exported_pkg_status(export_folder)
            print("vcpkg export {} successfully".format(packages))
        else:
            export_folder = None
            print("vcpkg export {} failed".format(packages))      
        return export_folder

    def import_pkg (self,export_folder):
        ret_code = True
        copy_tree(export_folder, self._vcpkg_root_path)
        self._vcpkg_pkg.load_exported_pkg_status()
        print("{} is imported to {} successfully".format(export_folder,self._vcpkg_root_path))
        return ret_code
