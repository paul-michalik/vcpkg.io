from conans import ConanFile

class {}{}(ConanFile):
    name = "{}"
    version = "{}"
    license = "GPL-3.0"
    url = "<https://github.com/apattnaik0721013/vcpkg>"
    description = "conan for vcpkg"
    settings = {}
    no_copy_source=True


    def package(self):
        self.copy(r"{}", dst="pkg", src=r"{}")