import os,platform,sys,time,yaml
from colorama import init,Fore
init(autoreset=True)

def print_message(input_str,type="",term='\n'):
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    
    if type.lower() == 'warning':
        print(YELLOW + input_str,end=term)
    elif type.lower() == 'error':
        print(RED + input_str,end=term)
    elif type.lower() == 'success':
        print(GREEN + input_str,end=term)
    else:
        print(input_str,end=term)

def system(command):
    if os.path.isfile("vcpkg.io.log" )==False:
        command += " > vcpkg.io.log"
    else:
        command += " >> vcpkg.io.log"
    ret_code=os.system(command)
    return ret_code