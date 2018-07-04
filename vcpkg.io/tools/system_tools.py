from conans import ConanFile,tools
import os,platform,sys,yaml,shutil

log_dir= os.path.dirname(os.path.abspath(__file__)) + os.sep + "log"
log_path= os.path.dirname(os.path.abspath(__file__)) + os.sep + "log"+ os.sep + "vcpkgio.log"

'''
    run batch command with log support on/off
'''
def run(command,log_support=True):
    if os.path.isdir(log_dir) == False:
        os.makedirs( log_dir, exist_ok=True)
    os.system("echo start %s >> %s" % (command,log_path))
    if log_support == True:                  
        command += " >> %s" % log_path
    ret_code=os.system(command)
    os.system("echo end  ... >> %s" % (log_path))
    return ret_code

def compress(src_path,dest_path):
    os.system(r'7z a %s.zip %s\* > nul 2>&1' % (src_path,dest_path))

def uncompress(zip_file,dest_path):
    os.system(r'cd /d %s && 7z x %s -aoa -o%s > nul 2>&1' % (dest_path,zip_file,dest_path))

def remove(folder_path,file_type=""):
    if not file_type:
        shutil.rmtree(folder_path)
    else:
        [os.remove(os.path.join(folder_path,f)) for f in os.listdir(folder_path) if f.find(file_type) != -1]

def extract_data(filename):
    data = {}
    status=False
    if os.path.isfile(filename )==True:
        status = True
        content=tools.load(filename)
        data=yaml.load(content)
    return status,data

def get_value(filen_name,string):
    value=""
    status = False
    if os.path.isfile(filen_name) == True:
        lines = tuple(open(filen_name, 'r'))
        for line in lines:
            find_string_index = line.find(string)
            if find_string_index != -1:
                find_string_index += len(string)
                value = line[find_string_index:-1]
                status = True
                break
    else:
        os.system('echo "%s is not created"' % filen_name)
    return status,value

def create_file(template_filename,filename,str_list):
    retcode = 1
    if os.path.isfile(template_filename) == True:
        template_content=tools.load(template_filename)
        template_content = template_content.format(*str_list)
        tools.save(filename,template_content)
        if os.path.isfile(filename) == False:
            os.system('echo %s is not created' % filename)
        else:
            retcode = 0
    else:
        os.system('echo %s is not found' % template_filename)
    if retcode == 1:
        raise RuntimeError("update %s failed!" % template_filename)

def getdata_from_yml(self,filename):
    data = {}
    status=False
    if os.path.isfile(filename )==True:
        status = True
        content=tools.load(filename)
        data=yaml.load(content)
    return status,data

def setdata_to_yml(filename,data):
    status=False
    content = ""
    for tag in data.keys():
        content += "%s: %s\r\n" % (tag,data[tag])
    tools.save(filename,content)
    return status

def update_setting_file(filename,setting):
    status = False
    if os.path.isfile(filename) == True:
        status,data = getdata_from_yml(filename)
        if status == True:
            setdata_to_yml(filename,setting)
    return status

def get_tree_size(path):
    """Return total size of files in path and subdirs. If
    is_dir() or stat() fails, print an error message to stderr
    and assume zero size (for example, file has been deleted).
    """
    total = 0
    for entry in os.scandir(path):
        try:
            is_dir = entry.is_dir(follow_symlinks=False)
        except OSError as error:
            print('Error calling is_dir():', error, file=sys.stderr)
            continue
        if is_dir:
            total += get_tree_size(entry.path)
        else:
            try:
                total += entry.stat(follow_symlinks=False).st_size
            except OSError as error:
                print('Error calling stat():', error, file=sys.stderr)
    return total

def count_subparts(path,folder_name):
    sub_dir_list = []
    search_file = "%s.7z" % folder_name
    for entry in os.scandir(path):
        if search_file in entry.name:
            sub_dir_list.extend([entry.name])
    return sub_dir_list

def compress_bin(upload_dir,folder_name):
    total_size_str = tools.human_size(get_tree_size(upload_dir))
    max_subdir_size = 100
    sub_part_list = []
    if "GB" in total_size_str:       
        os.system('cd /d %s && 7z.exe a -v%sm %s > nul' % (upload_dir,max_subdir_size,folder_name))
    else:
        os.system('cd /d %s && 7z.exe a %s > nul' % (upload_dir,folder_name))
    sub_part_list = count_subparts(upload_dir,folder_name)
    return sub_part_list