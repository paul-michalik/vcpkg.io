import os,platform,sys,time
from util import (print_message,system)
import wget
import zipfile

class Command(object):
    """ A single command of the conan application, with all the first level commands.
    Manages the parsing of parameters and delegates functionality in
    collaborators.
    It can also show help of the tool
    """
    def __init__(self):
        self._default_vcpkg_path = "https://github.com/Microsoft/vcpkg.git"
        self._default_directory = "vcpkg.io/vcpkg"
        self._default_vcpkg_url = "https://github.com/Microsoft/vcpkg"
        self._method = {}
        self._method["help"] = self._help
        self._method["clone"] = self._clone
        self._method["pull"] = self._pull
        self._method["download"] = self._download            

    def _help(self, args):
        """Show help of a specific commmand.
        """
        if len(args) <= 1 or "all" == args[1]:
            print("commands: vcpkg.io")
            print('vcpkg.io clone [<repository> <directory>]')
            print('         - default repository is https://github.com/Microsoft/vcpkg.git')
            print('         - default directory is vcpkg.io/vcpkg')
            print('vcpkg.io pull <directory>')
            print('         - default directory is vcpkg.io/vcpkg')
            print('vcpkg.io download <revision> [url]')
            print('         - default url is https://github.com/Microsoft/vcpkg.git')
        elif  "clone" == args[1]:
            print("commands: vcpkg.io clone")
            print('vcpkg.io clone [<repository> <directory>]')
            print('         - default repository is https://github.com/Microsoft/vcpkg.git')
            print('         - default directory is vcpkg.io/vcpkg')
        elif  "pull" == args[1]:
            print("commands: vcpkg.io pull")
            print('vcpkg.io pull <directory>')
            print('         - default directory is vcpkg.io/vcpkg')
        elif  "download" == args[1]:
            print("commands: vcpkg.io download")
            print('vcpkg.io download <revision> [url]')
            print('         - default url is https://github.com/Microsoft/vcpkg.git')

    def _clone(self, args):
        """clone from vcpkg repositry
        """
        if len(args) <= 1:
            param = self._default_vcpkg_path + " " + self._default_directory
        else:
            param = ' '.join(args[1:])
        return system("git clone %s" % param)

    def _pull(self, args):
        """Pulls changes from upstream 
        """
        
        if len(args) <= 1:
            param = self._default_directory
        else:
            param = ' '.join(args[1:])
        print("git pull %s" % param)
        return system("git pull %s" % param)

    def _download(self, args):
        """Pulls changes from upstream 
        """
        if len(args) <= 1:
            print("few argument provided")
            self._help(["help", "download"])
            return 1
        elif len(args) <= 2:
            tag=args[1]
            url = self._default_vcpkg_url
        else:
            tag=args[1]
            url = args[2]
        url = url + "/archive/"+tag+".zip"
        testfile= wget.download(url)

        with zipfile.ZipFile(testfile,"r") as zip_ref:
            zip_ref.extractall(".")
        return 

    def run(self, args):
        """HIDDEN: entry point for executing commands, dispatcher to class
        methods
        """
        errors = False
        try:
            try:  
                method = self._method[args[0]]      
            except KeyError as exc:
                self._help(["help"])
                raise Exception("Unknown command %s" % str(exc))
            except IndexError:  # No parameters
                self._help(["help"])
                return False
            method(args)
        except KeyboardInterrupt as exc:
            errors = True
        except SystemExit as exc:
            if exc.code != 0:
                errors = True
        except Exception as exc:
            import traceback
            print(traceback.format_exc())
            errors = True
        return errors

def main(args):
    """ main entry point of the vcpkgio application, using a Command to
    parse parameters

    Exit codes for conan command:

        0: Success (done)
        1: General ConanException error (done)
        2: Migration error
        3: Ctrl+C
        4: Ctrl+Break
    """
    command = Command()
    current_dir = os.getcwd()
    try:
        import signal

        def ctrl_c_handler(_, __):
            print('You pressed Ctrl+C!')
            sys.exit(3)

        def ctrl_break_handler(_, __):
            print('You pressed Ctrl+Break!')
            sys.exit(4)

        signal.signal(signal.SIGINT, ctrl_c_handler)
        if sys.platform == 'win32':
            signal.signal(signal.SIGBREAK, ctrl_break_handler)
        error = command.run(args)
    finally:
        os.chdir(current_dir)
    sys.exit(error)