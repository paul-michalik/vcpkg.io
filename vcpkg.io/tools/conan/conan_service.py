import os,platform,sys,yaml
from os import path
from tools import system_tools,vcpkgio_config
from conans import tools

class conan:
    def __init__(self,setting):
        self._setting = vcpkgio_config.vcpkgio_config(setting)    
        self._conan_root = os.path.dirname(os.path.abspath(__file__))
        self._conan_cmd={}
        self._config_dir= self._conan_root + os.sep + "config"
        self._temp_dir= self._conan_root + os.sep + "temp"
        self._init_conan_cmd()
        self._init_conan_config()

    def _init_conan_cmd(self):
        self._conan_cmd["config"] = "conan config install %s.zip"
        self._conan_cmd["info"] =  "conan info %s %s > %s"
        self._conan_cmd["create"] = "conan create %s %s/%s %s -k"
        self._conan_cmd["user"] = "conan user -p %s -r vcpkgrepository %s"
        self._conan_cmd["upload"] = "conan upload %s -p %s -r vcpkgrepository -c --force"
        self._conan_cmd["install"] = "conan install %s --install-folder %s %s --build=never -u"
    
    def _init_conan_config(self):             
        system_tools.setdata_to_yml(os.path.join(self._config_dir,"settings.yml"),self._setting.get_binary_setting())
        tools.save(self._config_dir + os.sep + "remotes.txt","vcpkgrepository " + self._setting.get_remote_setting('repository_url')) 
        default_file = self._config_dir + os.sep + "profiles"+ os.sep + "default"        
        default_setting_value = self._setting.get_setting_str('binary_setting',postfix='={}\n')
        default_setting_list = "[build_requires]\n[options]\n[env]\n[settings]\n"+ default_setting_value
        tools.save(default_file,default_setting_list)

    '''
        run conan command
    '''
    def _run_conan_cmd(self,command,tup=()):
        
        conan_cmd = self._conan_cmd[command]        
        if len(tup):
            conan_cmd = self._conan_cmd[command] % (tup)
        if "upload" == command or "info" == command:
            ret_code = system_tools.run (conan_cmd,False)
        else:        
            ret_code = system_tools.run (conan_cmd)
        return ret_code

    '''
    extract installed conan pkg id
    '''
    def _get_conan_pkg_id(self):
        info_recipe_file = self._temp_dir + os.sep + "conanfile.py"
        info_recipe_template = self._conan_root + os.sep + "conan_info_recipe_templete.py"
        recipe_info = self.parse_conan_repo(self._setting.get_remote_setting('repository_name'))
        conan_pkg_setting = self._setting.get_setting_str('binary_setting',prefix="'",infix=",'",postfix="'")      
        recipe_info.extend([conan_pkg_setting])
        system_tools.create_file(info_recipe_template,info_recipe_file,recipe_info)
        conan_pkg_info_file = self._temp_dir+ os.sep + "depend.txt"
        conan_setting_val = self._setting.get_setting_str('binary_setting',prefix="-s ",infix=" -s ",postfix='={}')
        self._run_conan_cmd("info",(self._temp_dir,conan_setting_val,conan_pkg_info_file))
        status,cur_package_id = system_tools.get_value(conan_pkg_info_file,"ID: ")
        system_tools.remove(self._temp_dir,".py")
        return status,cur_package_id

    '''
    update conan config
    '''   
    def _update_conan_config(self):
        if os.path.isdir(self._config_dir) == True:
            conan_setting_file = os.path.join(self._config_dir,"settings.yml")
            system_tools.setdata_to_yml(conan_setting_file,self._setting.get_binary_setting())            
            system_tools.compress(self._config_dir,self._config_dir)
            self._run_conan_cmd("config",(self._config_dir))            
            system_tools.remove(self._conan_root,'.zip')
        else:
             print("setting failed . %s not found" % self._config_dir)


    '''
    create conan upload recipe
    '''
    def _create_conan_upload_recipe(self,upload_dir,upload_file):
        recipe_info = self.parse_conan_repo(self._setting.get_remote_setting('repository_name'))      
        conan_pkg_setting = self._setting.get_setting_str('binary_setting',prefix="'",infix=",'",postfix="'")
        recipe_info.extend([conan_pkg_setting])   
        recipe_info.extend([upload_file])
        recipe_info.extend([upload_dir])   
        system_tools.create_file(os.path.join(self._conan_root,"conan_upload_recipe_templete.py"),os.path.join(self._temp_dir,"conanfile.py"),recipe_info)

    '''
    create conan package
    '''
    def _create_conan_pkg(self,sub_part=0):
        repo_info = self.parse_conan_repo(self._setting.get_remote_setting('repository_name'))
        self._setting.set_binary_setting('sub_parts',[str(sub_part)] )
        self._update_conan_config()
        conan_setting_val = self._setting.get_setting_str('binary_setting',prefix="-s ",infix=" -s ",postfix='={}')
        self._run_conan_cmd("create",(self._temp_dir,repo_info[0],repo_info[1],conan_setting_val))

    '''
    upload conan package to bintray
    '''
    def _upload_conan_pkg_to_bintray(self,sub_part):
        ret_code =1
        status,conan_pkg_id=self._get_conan_pkg_id()
        if status == True:
            self._run_conan_cmd("user",(self._setting.get_remote_setting('password'),self._setting.get_remote_setting('username') ))
            ret_code=self._run_conan_cmd("upload",(self._setting.get_remote_setting('repository_name'),conan_pkg_id)) 
        return ret_code

    '''
    create conan package and upload conan package to bintray
    '''
    def _conan_upload(self,bin_folder,bin_file,sub_part=0):
        os.makedirs(self._conan_root + os.sep + "temp", exist_ok=True)
        self._create_conan_upload_recipe(bin_folder,bin_file)        
        self._create_conan_pkg(sub_part)
        self._upload_conan_pkg_to_bintray(sub_part)
        system_tools.remove(self._temp_dir)

    def _conan_download(self,download_folder):
        os.makedirs(self._conan_root + os.sep + "temp", exist_ok=True)
        self._create_conan_download_recipe(download_folder)
        download_subpart = ret_code = 0
        while ret_code == 0:
            self._setting.set_binary_setting('sub_parts',[str(download_subpart)] )
            self._update_conan_config()
            status,conan_pkg_id=self._get_conan_pkg_id()
            if status:
                conan_setting_val = self._setting.get_setting_str('binary_setting',prefix="-s ",infix=" -s ",postfix='={}') 
                ret_code=self._run_conan_cmd("install",(self._temp_dir,download_folder,conan_setting_val))
                download_subpart += 1
            else:
                break
        system_tools.remove(self._temp_dir)

    '''
    create conan download recipe
    '''
    def _create_conan_download_recipe(self,download_folder):
        download_recipe_file = self._temp_dir + os.sep + "conanfile.txt"
        download_recipe_template = self._conan_root + os.sep + "conan_download_recipe_template.txt"
        system_tools.create_file(download_recipe_template,download_recipe_file,[self._setting.get_remote_setting('repository_name'),download_folder])

    def parse_conan_repo(self,repository):
        valid_repository = False
        packagename=packageversion=user=channel=""        
        findindex = repository.find("/")
        if findindex != -1:
            packagename,str_list,channel = repository.split("/")
            findindex = str_list.find("@")
            if findindex != -1:
                valid_repository = True
                packageversion,user = str_list.split("@")
        if valid_repository == False:
                raise RuntimeError("invalid conan repository!")
        return [user,channel,packagename,packageversion]